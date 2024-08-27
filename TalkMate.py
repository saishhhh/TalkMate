import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import io
import sounddevice as sd
import numpy as np
import wavio

# Popular languages for translation
LANGUAGES = {
    'Hindi': 'hi',
    'French': 'fr',
    'Spanish': 'es',
    'German': 'de',
    'Chinese': 'zh-cn',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Russian': 'ru',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Arabic': 'ar',
    'Turkish': 'tr',
    'Dutch': 'nl',
    'Swedish': 'sv'
}

# Function to record audio
def record_audio(duration=10, fs=44100):
    st.write("Recording...")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    return audio_data, fs

# Function to save audio as a .wav file
def save_audio(audio_data, fs, filename="output.wav"):
    wavio.write(filename, audio_data, fs, sampwidth=2)

def main():
    st.title("Language Translator")

    # Language selection
    language = st.selectbox("Choose a language to translate to:", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[language]

    # Option to choose between audio or text input
    input_method = st.radio("Choose input method:", ("Audio", "Text"))

    if input_method == "Audio":
        if st.button("Record and Translate"):
            # Record audio
            audio_data, fs = record_audio(duration=10)
            save_audio(audio_data, fs)

            # Recognize speech
            r = sr.Recognizer()
            translator = Translator()
            with sr.AudioFile("output.wav") as source:
                audio = r.record(source)
                try:
                    speech_text = r.recognize_google(audio)
                    st.write(f"Recognized text: {speech_text}")

                    # Translate the recognized text
                    translated_text = translator.translate(speech_text, dest=lang_code).text
                    st.write(f"Translated text: {translated_text}")

                    # Convert translated text to speech
                    voice = gTTS(translated_text, lang=lang_code)
                    audio_bytes = io.BytesIO()
                    voice.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)

                    # Display the audio player
                    st.audio(audio_bytes, format='audio/mp3')

                except sr.UnknownValueError:
                    st.error("Couldn't understand. Please try again.")
                except sr.RequestError as e:
                    st.error(f"Error with the speech recognition service; {e}")

    elif input_method == "Text":
        text_input = st.text_area("Enter text to translate:")
        if st.button("Translate"):
            if text_input:
                translator = Translator()
                translated_text = translator.translate(text_input, dest=lang_code).text
                st.write(f"Translated text: {translated_text}")

                # Convert translated text to speech
                voice = gTTS(translated_text, lang=lang_code)
                audio_bytes = io.BytesIO()
                voice.write_to_fp(audio_bytes)
                audio_bytes.seek(0)

                # Display the audio player
                st.audio(audio_bytes, format='audio/mp3')
            else:
                st.warning("Please enter some text.")

    # Footer text
    st.markdown("""
        <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            text-align: center;
            padding: 10px;
            color: #999;
            font-size: 12px;
        }
        </style>
    

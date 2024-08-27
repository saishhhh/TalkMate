import streamlit as st
from google.cloud import speech
import google.auth
from googletrans import Translator
from gtts import gTTS
import io
import pyaudio

# Google Cloud setup
credentials, project = google.auth.default()
client = speech.SpeechClient(credentials=credentials)

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

def main():
    st.title("Real-Time Language Translator")

    # Language selection
    language = st.selectbox("Choose a language to translate to:", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[language]

    # Stream from the microphone
    if st.button("Start Listening and Translate"):
        st.write("Listening...")

        # Set up the microphone and stream
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

        # Google Cloud Speech API configuration
        streaming_config = speech.StreamingRecognitionConfig(
            config=speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="en-US"
            ),
            interim_results=True
        )

        # Generator function to stream audio
        def generate_audio():
            while True:
                data = stream.read(1024)
                yield speech.StreamingRecognizeRequest(audio_content=data)

        # Perform real-time speech recognition
        responses = client.streaming_recognize(config=streaming_config, requests=generate_audio())

        # Handle the responses
        for response in responses:
            if response.results and response.results[0].alternatives:
                speech_text = response.results[0].alternatives[0].transcript
                st.write(f"Recognized text: {speech_text}")

                # Translate the recognized text
                translator = Translator()
                translated_text = translator.translate(speech_text, dest=lang_code).text
                st.write(f"Translated text: {translated_text}")

                # Convert translated text to speech
                voice = gTTS(translated_text, lang=lang_code)
                audio_bytes = io.BytesIO()
                voice.write_to_fp(audio_bytes)
                audio_bytes.seek(0)

                # Display the audio player
                st.audio(audio_bytes, format='audio/mp3')

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
        <div class="footer">
            Developed by Saish M Patil
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import io

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
    st.title("Speech Translator")

    # Language selection
    language = st.selectbox("Choose a language to translate to:", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[language]

    if st.button("Record and Translate"):
        st.write("Listening...")
        r = sr.Recognizer()
        translator = Translator()

        with sr.Microphone() as source:
            audio = r.listen(source)
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

                # Option to replay the audio
                if st.button("Replay"):
                    st.audio(audio_bytes, format='audio/mp3')

            except sr.UnknownValueError:
                st.error("Couldn't understand. Please try again.")
            except sr.RequestError as e:
                st.error(f"Error with the speech recognition service; {e}")

if __name__ == "__main__":
    main()

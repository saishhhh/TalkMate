import streamlit as st
from googletrans import Translator
from gtts import gTTS
import io

# Popular languages for translation
LANGUAGES = {
    'Hindi': 'hi',
    'French': 'fr',
    'Spanish': 'es',
    'Arabic': 'ar',
    'Japanese': 'ja',
    'Russian': 'ru',
    'German': 'de',
    'Chinese': 'zh-cn',
    'Italian': 'it',
}

def main():
    st.title("Language Translator")

    # Language selection
    language = st.selectbox("Choose a language to translate to:", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[language]

    # Text input for translation
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
        <div class="footer">
            Developed by Saish M Patil
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

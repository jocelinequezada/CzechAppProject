# Joceline Quezada
# 06/14/2025
import streamlit as st
from deep_translator import GoogleTranslator
import pronouncing
import openai

# Set your OpenAI API key (replace with your own or set via Streamlit secrets)
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "your-openai-api-key"

st.title("Czech ↔ English Translator with Pronunciation")

# User input
text_input = st.text_input("Enter Czech or English text:")
direction = st.selectbox("Translation Direction", ["Czech to English", "English to Czech"])

def translate_with_openai(text, source_lang, target_lang):
    prompt = f"Translate this from {source_lang} to {target_lang}: {text}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"OpenAI translation failed: {str(e)}"

def get_english_pronunciation(text):
    words = text.split()
    pronunciations = []
    for word in words:
        phones = pronouncing.phones_for_word(word.lower())
        if phones:
            pronunciations.append(phones[0])
        else:
            pronunciations.append(word)
    return " | ".join(pronunciations)

# Translate button
if st.button("Translate"):
    if text_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        src_lang = 'cs' if direction == "Czech to English" else 'en'
        tgt_lang = 'en' if src_lang == 'cs' else 'cs'

        try:
            translated = GoogleTranslator(source=src_lang, target=tgt_lang).translate(text_input)
        except Exception as e:
            st.warning("Google Translate failed. Trying OpenAI...")
            translated = translate_with_openai(text_input, "Czech" if src_lang == 'cs' else "English",
                                               "English" if tgt_lang == 'en' else "Czech")

        st.success("**Translation:**")
        st.write(translated)

        if direction == "Czech to English":
            st.info("**English Pronunciation (approximate phonemes):**")
            pronunciation = get_english_pronunciation(translated)
            st.code(pronunciation)

import openai
import streamlit as st
from googletrans import Translator

# Set your OpenAI API key
openai.api_key = 'your-openai-api-key'

translator = Translator()

def is_czech(text):
    czech_chars = "áčďéěíňóřšťúůýž"
    return any(char in text.lower() for char in czech_chars)

def fallback_translation(text, src, dest):
    try:
        translated = translator.translate(text, src=src, dest=dest)
        return translated.text
    except Exception as e:
        return f"[Fallback error: {e}]"

def openai_translate_and_ipa(text, source_lang):
    prompt = f"""
You're a bilingual Czech ↔ English tutor.

Task:
1. Translate the input sentence to the other language.
2. Correct any grammar mistakes (if there are any).
3. Show the pronunciation of the corrected sentence using IPA.

Input: {text}
Language: {"Czech" if source_lang == "cs" else "English"}

Respond clearly with:
- Corrected sentence
- Translated sentence
- IPA pronunciation
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return None

# --- Streamlit UI ---
st.set_page_config(page_title="Czech ↔ English Language Tutor", page_icon="🌍")
st.title("🧠 Czech ↔ English Tutor")
st.write("Enter a sentence in Czech or English. The app will correct it, translate it, and show IPA pronunciation.")

user_input = st.text_area("✍️ Your sentence:", height=100)

if st.button("Translate & Explain"):
    if not user_input.strip():
        st.warning("Please enter a sentence.")
    else:
        lang_code = 'cs' if is_czech(user_input) else 'en'
        opposite_lang = 'en' if lang_code == 'cs' else 'cs'

        st.info("Using GPT to process your input...")
        result = openai_translate_and_ipa(user_input, lang_code)

        if result:
            st.success("✅ Tutor Result:")
            st.markdown(result)
        else:
            translated = fallback_translation(user_input, src=lang_code, dest=opposite_lang)
            st.error("⚠️ GPT failed. Showing fallback result using Google Translate:")
            st.write(f"➡️ Translated: {translated}")

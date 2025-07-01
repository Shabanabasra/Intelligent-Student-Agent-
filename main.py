import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Streamlit page config
st.set_page_config(page_title="🧠 Intelligent Student Agent", layout="wide")

# App Title
st.title("🤖 Intelligent Student Agent")

# Tool options (radio in column by default)
option = st.radio("Choose Tool:", [
    "📘 Academic Q&A",
    "🧠 Study Tips",
    "📝 Text Summary",
    "🧪 MCQ Generator",
    "📌 Flashcards",
    "💡 Concept Simplifier"
], index=0)

# Topic input
topic = st.text_input("Enter a topic", placeholder="e.g. Newton's Laws of Motion")

# Generate button
if st.button("🚀 Generate Response"):
    if not topic.strip():
        st.warning("⚠️ Please enter a topic.")
    else:
        # Adjust prompt based on selected tool
        prompt = f"Explain in detail: {topic}"
        if option == "🧠 Study Tips":
            prompt = f"Give 5 study tips for: {topic}"
        elif option == "📝 Text Summary":
            prompt = f"Summarize the topic '{topic}' in 5 bullet points."
        elif option == "🧪 MCQ Generator":
            prompt = f"Generate 5 multiple choice questions with answers for: {topic}"
        elif option == "📌 Flashcards":
            prompt = f"Create 5 flashcards (Q&A format) for: {topic}"
        elif option == "💡 Concept Simplifier":
            prompt = f"Explain the concept of '{topic}' in very simple language suitable for a 10-year-old."

        # OpenRouter request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": "You are an intelligent and friendly tutor."},
                {"role": "user", "content": prompt}
            ]
        }

        try:
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
            result = res.json()

            if res.status_code == 200:
                content = result["choices"][0]["message"]["content"]
                st.markdown(content)
            else:
                st.error(f"❌ Error {res.status_code}: {result}")
        except Exception as e:
            st.error(f"⚠️ Failed to generate response: {str(e)}")

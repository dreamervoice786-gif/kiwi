
import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

st.set_page_config(
    page_title="Groq AI Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #240046, #5a189a, #7b2cbf);
        color: white;
    }

    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.10);
        border-radius: 12px;
        padding: 12px;
    }

    [data-testid="stChatInput"] {
        background-color: #ffffff;
    }

    h1, p {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🤖 Groq AI Chatbot")
st.caption("Powered by Groq API")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is missing. Add it to your .env file.")
    st.stop()

client = Groq(api_key=api_key)

MODEL = "qwen/qwen3.8-27"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant. Be clear and concise.",
        }
    ]

if st.button("🗑️ Clear Chat"):
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant. Be clear and concise.",
        }
    ]
    st.rerun()

for message in st.session_state.messages:
    if message["role"] in ("user", "assistant"):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=1024,
                )

                answer = response.choices[0].message.content
                st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as error:
            st.error(f"Groq API error: {error}")
            st.session_state.messages.pop()

import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

from prompts import build_prompt

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="🎓",
    layout="centered"
)

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key is not configured.")
    st.stop()

client = genai.Client(api_key=api_key)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🎓 StudyMate AI")
st.write("Your AI-powered study assistant")


# --------------------------------------------------
# FEATURE SELECTION
# --------------------------------------------------

feature = st.selectbox(
    "What would you like StudyMate AI to do?",
    [
        "Summarize Notes",
        "Explain a Concept",
        "Generate Quiz",
        "Improve an Answer"
    ]
)


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

user_input = st.text_area(
    "Enter your content",
    placeholder="Paste your notes, question, topic, or answer here...",
    height=250
)


# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

if st.button("✨ Generate", use_container_width=True):

    # Input validation
    if not user_input.strip():
        st.warning("Please enter some content before generating a response.")

    else:

        # Build structured prompt
        prompt = build_prompt(feature, user_input)

        try:

            # Show loading message
            with st.spinner("StudyMate AI is thinking..."):

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

            # Display result
            st.caption(
                "Choose a study task, provide your content, and let StudyMate AI help you learn."
            )
            st.divider()
            st.subheader("🤖 AI Generated Result")

            st.write(response.text)

        except Exception as e:
            error_message = str(e)
            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                st.warning(
                    "⚠️ Gemini API quota has been temporarily exhausted. "
                    "Please try again later."
                )
            elif "503" in error_message or "UNAVAILABLE" in error_message:
                st.warning(
                    "⚠️ Gemini is temporarily unavailable. "
                    "Please try again later."
                )
            else:
                st.error("Something went wrong while generating the response.")
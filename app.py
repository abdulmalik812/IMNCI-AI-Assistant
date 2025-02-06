import streamlit as st
import speech_recognition as sr
from models.imnci_llm import classify_symptoms  # Import function from imnci_llm.py

# Streamlit UI Setup
st.set_page_config(page_title="IMNCI AI Assistant", layout="wide")
st.title("👶 IMNCI AI Assistant for ANM / Field worker")

st.write("""
### 🏥 Voice-Assisted IMNCI Classification
Simply **speak** or **type** the newborn's symptoms, and our AI will provide a structured IMNCI chart with **classification & treatment plans**.
""")

# Initialize session state for symptoms
if "symptoms_text" not in st.session_state:
    st.session_state["symptoms_text"] = ""

# Function to record voice input
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Speak Now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        st.session_state["symptoms_text"] = text  # Store voice input in session state
        st.success(f"🗣️ You said: {text}")
    except sr.UnknownValueError:
        st.error("❌ Sorry, could not understand the audio.")
    except sr.RequestError:
        st.error("❌ Could not request results from Google Speech API.")

# User input section
col1, col2 = st.columns([3, 2])

with col1:
    # Use `value=` instead of `key=`
    symptoms_text = st.text_area("✍️ Enter Symptoms (or use voice input)", 
                                 value=st.session_state["symptoms_text"], 
                                 height=150)  

    if st.button("🎙️ Use Voice Input"):
        get_voice_input()  # Capture voice input and update session state
        st.rerun()  # Force a rerun so the UI updates with the new voice text

    if st.button("🩺 Analyze Symptoms"):
        if symptoms_text:
            result = classify_symptoms(symptoms_text)
            st.subheader("📋 IMNCI Classification & Treatment Plan")
            st.markdown(result, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please enter symptoms before analyzing.")


    #st.image("assets/nurse_assistant.png", use_column_width=True)
    

st.markdown("---")
st.write("🤖 Powered by Google Gemini AI | 🔬 Based on WHO's IMNCI Guidelines")

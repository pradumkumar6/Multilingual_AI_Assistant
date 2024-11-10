import speech_recognition as sr
import logging
import os
from gtts import gTTS
import google.generativeai as genai
import streamlit as st

# Create a logger
LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"

os.makedirs(LOG_DIR, exist_ok=True)

log_path = os.path.join(LOG_DIR,LOG_FILE_NAME)

logging.basicConfig(
    filename=log_path,
    format = "[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level= logging.INFO
)


def takeCommand():
    """This function takes command & recognize

    Returns:
        text as query
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language="en-in")
        print(f"User said: {query}\n")
    except Exception as e:
        logging.info(e)
        print("Say that again please")
        return "None"
    return query

# takeCommand()


def text_to_speech(text):
    ttx = gTTS(text=text,lang="en")
    ttx.save("speech.mp3")

# text = takeCommand()
# text_to_speech(text)

def gemini_model(user_input):
    genai.configure(api_key="your_api_key_here")
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_input)
    results = response.text
    return results

text = takeCommand()
res = gemini_model(text)
# print(res)
text_to_speech(res)



def main():
    st.title("Multilingual AI Assistant")
    if st.button("Ask me anything!"):
        with st.spinner("Listening..."):
            text = takeCommand()
            # print(text)
            response = gemini_model(text)
            text_to_speech(response)

            # Display audio player and download link
            audio_file = open("speech.mp3", "rb")
            audio_bytes = audio_file.read()

            st.text_area(label="Response",value=response,height=350)
            st.audio(audio_bytes,format="audio/mp3")
            st.download_button(label="Download Speech",data=audio_bytes,file_name="speech.mp3",mime="audio/mp3")


main()
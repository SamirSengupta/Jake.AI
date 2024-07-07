import os
import speech_recognition as sr
import pyttsx3
from groq import Groq as Jake
from secret import key, prompt
import streamlit as st

# Set your Groq API key here if not using environment variable
API_KEY = key

# Initialize Groq client
client = Jake(api_key=API_KEY)

# Initialize conversation history
conversation_history = [
    {
        "role": "system",
        "content": prompt
    }
]

def get_response_from_groq(message):
    global conversation_history

    # Update conversation history with formatted user input
    formatted_message = f"<{message}>"
    conversation_history.append({"role": "user", "content": formatted_message})
    if len(conversation_history) > 11:  # Keeping initial system prompt + 25 pairs (user and AI responses)
        conversation_history = conversation_history[-50:]

    try:
        chat_completion = client.chat.completions.create(
            messages=conversation_history,
            model="mixtral-8x7b-32768",
        )
        ai_response = chat_completion.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": ai_response})
        if len(conversation_history) > 26:
            conversation_history = conversation_history[-50:]
        return ai_response
    except Exception as e:
        return f"Error getting response from Groq: {e}"

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

import time

def speech_to_text():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        # Adjust for ambient noise and improve accuracy
        recognizer.adjust_for_ambient_noise(source)
        st.write("Jake.ai is listening:")

        start_time = time.time()
        audio = recognizer.listen(source, timeout=30)
        end_time = time.time()

        if end_time - start_time > 26   :
            return "Sorry, you took too long to speak."

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I could not understand you."
    except sr.RequestError:
        return "Sorry, there was an error with the request."
def main():
    st.set_page_config(page_title="Jake.ai", page_icon=":robot:", layout="wide")
    st.title("Jake.ai - Conversational AI")
    user_input = st.button("Start Conversation")

    if user_input:
        while True:
            user_text = speech_to_text()
            st.write(f"You said: {user_text}")

            # Check if user wants to exit
            if user_text.lower() == "code exit":
                st.write("Good Bye! Jake.ai is exiting.")
                break

            # Get response from Groq
            ai_response = get_response_from_groq(user_text)
            st.write(f"AI response: {ai_response}")

            # Convert AI response to speech
            text_to_speech(ai_response)

if __name__ == "__main__":
    main()
import os
import speech_recognition as sr
import pyttsx3
from groq import Groq
from secret import key, prompt
# Set your Groq API key here if not using environment variable
API_KEY = key

# Initialize Groq client
client = Groq(api_key=API_KEY)

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
    if len(conversation_history) > 11:  # Keeping initial system prompt + 5 pairs (user and AI responses)
        conversation_history = conversation_history[-50:]

    try:
        chat_completion = client.chat.completions.create(
            messages=conversation_history,
            model="mixtral-8x7b-32768",
        )
        ai_response = chat_completion.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": ai_response})
        if len(conversation_history) > 11:
            conversation_history = conversation_history[-50:]
        return ai_response
    except Exception as e:
        return f"Error getting response from Groq: {e}"

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        # Adjust for ambient noise and improve accuracy
        recognizer.adjust_for_ambient_noise(source)
        print("Please say something:")

        # Continuously listen until silence or timeout
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=1000)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        return "Sorry, there was an error with the speech recognition service."

def main():
    while True:
        # Capture speech from user
        user_input = speech_to_text()
        print(f"You said: {user_input}")

        # Check if user wants to exit
        if user_input.lower() == "code exit":
            print("Exiting the program.")
            break

        # Get response from Groq
        ai_response = get_response_from_groq(user_input)
        print(f"AI response: {ai_response}")

        # Convert AI response to speech
        text_to_speech(ai_response)

if __name__ == "__main__":
    main()

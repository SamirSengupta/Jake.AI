import os
import speech_recognition as sr
import pyttsx3
from groq import Groq as Jake
from secret import key, prompt
import streamlit as st
import time
from PIL import Image, ImageDraw, ImageOps

# Set your Groq API key here if not using environment variable
API_KEY = key

# Initialize Groq client
client = Jake(api_key=API_KEY)

# Initialize conversation history
conversation_history = [{"role": "system", "content": prompt}]

def get_response_from_groq(message, model):
    global conversation_history

    # Update conversation history with formatted user input
    formatted_message = f"<{message}>"
    conversation_history.append({"role": "user", "content": formatted_message})
    if len(conversation_history) > 26:  # Keeping initial system prompt + 25 pairs (user and AI responses)
        conversation_history = conversation_history[-50:]

    try:
        chat_completion = client.chat.completions.create(
            messages=conversation_history,
            model=model,
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

def speech_to_text():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        # Adjust for ambient noise and improve accuracy
        recognizer.adjust_for_ambient_noise(source)
        st.write("Jake is listening:")

        while True:
            audio = recognizer.listen(source, timeout=None)
            try:
                return recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                return "Sorry, I could not understand you."
            except sr.RequestError:
                return "Sorry, there was an error with the request."

def main():
    st.set_page_config(page_title="Jake.ai", page_icon=":robot:", layout="wide")
    st.title("Jake.ai - Conversational AI")

    tabs = st.tabs(["Conversation", "Benchmark", "About Dev"])

    # Conversation tab
    with tabs[0]:
        # Create a sidebar with options
        with st.sidebar:
            model_options = {
                "Mixtral 8x7b (Mistral)": "mixtral-8x7b-32768",
                "Gemma2 9b (Google)": "gemma2-9b-it",
                "LLaMA3 70b (Meta)": "llama3-70b-8192",
                "LLaMA3.1 8b (Beta)" : "llama-3.1-8b-instant",
            }
            selected_model = st.selectbox("Select Model", list(model_options.keys()))

        user_input = st.button("Start Conversation")

        if user_input:
            while True:
                user_text = speech_to_text()
                st.write(f"You said: {user_text}")

                # Check if user wants to exit
                if user_text.lower() == "code exit":
                    ai_response = get_response_from_groq("exit", model_options[selected_model])
                    st.write(f"AI response: {ai_response}")
                    text_to_speech(ai_response)
                    break
                # Get response from Groq
                ai_response = get_response_from_groq(user_text, model_options[selected_model])
                st.write(f"AI response: {ai_response}")

                # Convert AI response to speech
                text_to_speech(ai_response)

    # Benchmark tab
    with tabs[1]:
        st.image("benchmark.jpg", caption="Model Performance Benchmark", use_column_width=True)
        st.markdown("This image shows the performance benchmark of the models used in this app.")
    # About Dev tab
    with tabs[2]:
        # Load and process profile picture
        profile_pic = Image.open("Profile.jpg")
        size = (300, 300)
        profile_pic = profile_pic.resize(size)

        # Create circular mask
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        del draw

        # Apply mask to profile picture
        output = ImageOps.fit(profile_pic, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)

        # Display profile picture
        st.image(output, caption='', width=150, use_column_width=False)

        st.write('# Samir Sengupta')
        st.write('Data Scientist')
        st.write('Mumbai, India | 8356075699 | samir843301003@gmail.com | [GitHub](https://github.com/SamirSengupta) | [LinkedIn](https://linkedin.com/in/samirsengupta/) | [Neural Thread](https://neuralthread.cloud/samir)')

        st.write('## Summary')
        st.write('Data Scientist with a Bachelor\'s in Data Science from the University of Mumbai and extensive experience in machine learning, Artificial Intelligence (AI), and cybersecurity. Achieved a 40% increase in threat detection accuracy and a 35% improvement in incident response times at Synradar. At Neural Thread, boosted forecast accuracy by 25% and reduced error rates by 30% with advanced machine learning models. Proficient in Python, SQL, Power BI, and various ML frameworks, with certifications in Data Analysis, Generative AI, and Machine Learning. Skilled in deploying innovative AI solutions and optimizing code bases for enhanced performance and efficiency. Adept at translating complex data into actionable insights to drive strategic decision-making.')

        st.write('## Education')
        st.write('**BACHELORS IN DATA SCIENCE.**')
        st.write('University of Mumbai, April 2023')
        st.write('Mumbai, India')
        st.write('Acquired Skills: Deep Learning, Machine Learning, Artificial Intelligence, Databases, Neural Networks, Large Language Model.')

        st.write('**Higher Secondary Education (Science).**')
        st.write('University of Mumbai')
        st.write('Acquired Skills: Chemistry, Information Technology, Physics, Mathematics, Statistics.')

        st.write('## Work Experience')
        st.write('**Software Developer, Synradar.**')
        st.write('April 2020 - Aug 2023 – July 2024')
        st.write('Mumbai, India')
        st.write('- Developed machine learning-based intrusion detection systems with Python, increasing threat detection accuracy by 40% and reducing response times by 25%.')
        st.write('- Automated threat analysis using ML algorithms, enhancing breach identification efficiency by 50%.')
        st.write('- Designed interactive security analytics dashboards with Python, leading to a 35% improvement in incident response times.')
        st.write('- Created and optimized ML models for anomaly detection, boosting the identification of unusual patterns and potential threats by 45%.')
        st.write('- Integrated LLaMA 3 for code generation, optimization, and security evaluation, improving code quality and assessment efficiency by 30%.')

        st.write('**Data Scientist, Neural Thread**')
        st.write('Jan 2022 – July 2023')
        st.write('- Created and implemented machine learning models to predict key business metrics, resulting in a 25% increase in forecast accuracy and driving data-driven decision-making and improved outcomes.')
        st.write('- Improved predictive model accuracy by 30% by leveraging advanced neural network architectures and tuning hyperparameters.')
        st.write('- Deployed scalable AI solutions in production environments, reducing error rates by 40% and delivering significant business value.')
        st.write('- Developed generative AI models for innovative solutions, including chatbots and content generation tools, increasing customer engagement by 35%.')
        st.write('- Optimized machine learning code bases, reducing computational time by 50% and resource usage by 40%.')

        st.write('## Projects')
        st.write('**Music Mate: Song Downloading System.**')
        st.write('May 2023')
        st.write('- Created a music downloader utilizing the Spotify API and Python Tube library to extract songs from Spotify playlists and YouTube videos.')
        st.write('- Constructed a Flask backend to manage API requests, enabling the downloading of songs based on user input.')
        st.write('- Developed a front-end interface using HTML, CSS, and JavaScript for user interaction and input of Spotify playlist or YouTube video URLs.')

        st.write('**Power BI: Sales Forecasting Dashboard.**')
        st.write('Jan 2024')
        st.write('- Created an interactive Power BI dashboard for sales forecasting, using advanced data analysis and visualization techniques to provide useful insights.')
        st.write('- Implemented powerful forecasting models to predict sales trends accurately, helping businesses optimize their strategies.')
        st.write('- Improved decision-making by presenting detailed sales analytics in an easy-to-use interface, making it simple for stakeholders to understand important insights.')

        st.write('**Resume Evaluator: Gemini LLM based Candidate Shortlisting.**')
        st.write('Feb 2024')
        st.write('- Developed a Flask application utilizing Google\'s Gemini Large Language Model (LLM) to effectively summarize documents like CVs and job descriptions.')
        st.write('- Created robust functionality allowing the generation of concise summaries for both job descriptions and CVs, providing valuable insights into candidate suitability for hiring decisions.')
        st.write('- Integrated feedback generation features to recommend enhancements for candidates\' professional profiles, thereby facilitating their career advancement.')

        st.write('**MedScan.ai: Medical Documents Scanner.**')
        st.write('March 2024')
        st.write('- Scans medical images to provide accurate and timely diagnoses, enhancing clinical decision-making.')
        st.write('- Combines visual and textual data inputs, offering comprehensive medical insights and a holistic view of patient health.')
        st.write('- Designed for seamless operation, making it easy for healthcare professionals to integrate into their workflows and improve patient care.')

        st.write('**Jake.ai: Conversational AI.**')
        st.write('July 2024')
        st.write('- Jake.AI leverages advanced open-source large language models like LLaMA 3, Gemma 2, and Mistral for enhanced conversational and generative capabilities.')
        st.write('- It is locally hosted on your server using LM Studio, ensuring that all data remains private and secure.')
        st.write('- The platform functions as an AI companion, offering robust conversational abilities and innovative generative features.')
        st.write('- As an open-source solution, Jake.AI promotes transparency and flexibility in its AI interactions and implementations.')

        st.write('## Skills & Certifications')
        st.write('**Technical Skills:** Proficient in Python (NumPy, Pandas, Scikit-learn, TensorFlow, Keras), SQL (MySQL, PostgreSQL), Tableau, Power BI, R programming, with expertise in Machine Learning, Deep Learning, Neural Networks, Data Processing, Artificial Intelligence, LLM (Large Language Models), Generative AI, and Langchain, RAG (Retrieval-Augmented Generation).')
        st.write('**Soft Skills:** Strong collaborative teamwork, effective communication, adept problem-solving, meticulous attention to detail, excellent time management, adaptable to change, committed to continuous learning, skilled in critical thinking, capable leadership, and analytical thinking.')
        st.write('**Certifications:** Google Certified Data Analyst, Generative AI from Google, Power BI, MySQL, Machine Learning, Large Language Models (LLMs) from DeepLearning.AI, Adobe Photoshop, Advanced Excel, Python, Machine Learning from Stanford University.')

if __name__ == "__main__":
    main()

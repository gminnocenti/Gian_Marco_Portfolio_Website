import random
import json
import pickle
import numpy as np
import nltk
import streamlit as st
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import streamlit as st
import streamlit.components.v1 as components
from multiapp import MultiApp
from Financial_Statements import FinVista
from Deep_seek_chatbot import deepseek_chatbot
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words (sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class (sentence):
    bow = bag_of_words (sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes [r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice (i['responses'])
            break
    return result

def chatbotsidebar():
    st.sidebar.title("Chatbot")

    # Introduction text
    intro_text = """
    👋 **Welcome to Gian's Chatbot!**
    I'm your virtual assistant here to make your experience seamless. Whether you have questions, need assistance, or just want to chat, I'm here 24/7. Feel free to ask me anything!\n
    🤖 **What I Can Help With:**
    - Provide information on Gian Marco's Interests, Credentials, and Skills.
    - Answer frequently asked questions.
    - Assist with troubleshooting.
    - Engage in friendly conversation!\n
    🌐 **Navigation Tips:**
    - Type your questions or commands in the chatbox.
    - Explore various topics using keywords.\n
    🔒 **Privacy Assurance:**
    Your privacy is important. I don't store personal information, and our conversation is secure.
    Now, how can I assist you today? Type your message below! ⬇️
    """

    # Display the introduction text
    st.sidebar.markdown(intro_text, unsafe_allow_html=True)
    session_state = st.session_state
    st.sidebar.divider()

    if not hasattr(session_state, "conversation_history"):
        session_state.conversation_history = []

    # Display the conversation history in the sidebar
    for item in session_state.conversation_history:
        st.sidebar.text(item)

    # Recommended questions in a dropdown
    recommended_questions = [
         "What is Gian Marco's work experience?",
        "What is Gian Marco's gpa or school average?",
         "major role in applaudo",
        "How can i get in contact with Gian Marco?","what are gian marco's passions or interests",
        "what are gian marcos' computational skills","list of important coursework"

        # Add more questions as needed
    ]

    # User chooses either a recommended question or enters a custom question
    user_choice = st.sidebar.radio("Choose an option:", ["Select a Recommended Question", "Enter Custom Question"])

    if user_choice == "Select a Recommended Question":
        selected_question = st.sidebar.selectbox("Select a Recommended Question", recommended_questions)
        if selected_question:
            # Assuming you have defined predict_class and get_response functions
            ints = predict_class(selected_question)
            res = get_response(ints, intents)
            session_state.conversation_history.append(f"You: {selected_question}\nBot: {res}")
            st.sidebar.write("Bot: "+ res)

    elif user_choice == "Enter Custom Question":
        # Text input for custom questions
        user_input = st.sidebar.text_input("Enter Custom Text:")
        if user_input:
            ints = predict_class(user_input)
            res = get_response(ints, intents)
            session_state.conversation_history.append(f"You: {user_input}\nBot: {res}")
            st.sidebar.write("Bot: "+ res)


def Introduction():
    
    st.header("Explore the World of Data Science, Mathematics, and Coding")

    # Introduction
    st.write("Are you ready to embark on a journey through the world of data science, mathematics, and the fascinating realm of coding? I am Gian Marco Innocenti, a passionate junior studying data science and mathematics, and I am thrilled to introduce you to my digital haven where my coding projects come to life.")
    st.write("This website serves as a window into my world, showcasing a collection of innovative coding projects and a wealth of information about me. Whether you're a fellow enthusiast in data science and mathematics, a potential collaborator, or simply curious about the digital frontier, you've come to the right place.")

    # What Awaits You Here
    st.subheader("What Awaits You Here:")
    st.write("- **Project Gallery:** Explore a diverse array of coding projects that reflect my journey through data science and mathematics. From data analysis to machine learning models and software development, each project tells a unique story of problem-solving, creativity, and technical skill.")
    st.write("- **About Me:** Dive into my background, educational journey, and personal interests that drive my passion for coding and the digital world. Discover the experiences and inspirations that have shaped me as a data science enthusiast.")
    st.write("- **Chatbot Companion:** Meet my virtual assistant, a chatbot trained to provide you with information about me and my projects. Ask questions, seek guidance, or simply engage in a conversation about the fascinating topics that drive my academic and personal interests.")
    st.write("- **Financial Analysis Dashboard:** Dive into the economic metrics of publicly traded companies to understan which alligns the most with your investing interests.")

    # Closing
    st.write("Whether you're here to admire the art of coding, seek insights into data science and mathematics, or engage in an enlightening conversation with my chatbot, I invite you to explore, learn, and connect with me on this digital adventure.")
    st.write("Thank you for visiting, and let's embark on this coding journey together!")
def contact_info():
    col1, col2, col3 = st.columns(3)

    with col1:
    
        st.link_button("Go to my LinkedIn Profile", "https://www.linkedin.com/in/gian-marco-innocenti-castellanos-672778235/")
    with col2:
        st.link_button("Go to my Github Profile", "https://github.com/gminnocenti")
    with col3:

        st.link_button("Email Me", "mailto:gminnocenti123@gmail.com")
st.title("Welcome to the Digital Portfolio of Gian Marco Innocenti")
contact_info()
st.divider()
Introduction()
#chatbotsidebar()



st.divider()
######################################### Personal Projects
st.header('Personal Projects')
st.write('Please Explore my Collection of Personal Projects')
st.subheader('Select one Project: ')
app = MultiApp()

# Add all your application here
app.add_app("GianBot Personal Chatbot", deepseek_chatbot)
app.add_app("FinVista Application for Financial Analysis using Yahoo Finance API", FinVista)

# The main app
app.run()




import os
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
import pdfplumber

# Function to initialize Groq model and chain
def initialize_groq_chain(model_name: str = "deepseek-r1-distill-llama-70b") -> tuple[ChatGroq, StrOutputParser, callable]:
    """
    Initialize the Groq model and chain with environment variables.
    
    Args:
        model_name (str): The name of the Groq model to use. Defaults to "deepseek-r1-distill-llama-70b".
    
    Returns:
        tuple: (deepseek model, parser, deepseek_chain)
    
    Raises:
        ValueError: If the API key is not found in the environment variables.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Retrieve the API key
    api_key = os.getenv('key')
    if not api_key:
        raise ValueError("API key not found. Please ensure 'key' is set in your .env file as 'key=your_api_key_here'.")
    
    # Initialize the Groq model
    deepseek = ChatGroq(api_key=api_key, model_name=model_name)
    
    # Attach parser to the model
    parser = StrOutputParser()
    deepseek_chain = deepseek | parser
    
    return deepseek, parser, deepseek_chain

# Web scraping function
def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ' '.join([p.get_text() for p in soup.find_all('p')])
        text = re.sub(r'\s+', ' ', text).strip()
        
        if not text:
            return None, "No meaningful content found on the page."
        
        document = Document(page_content=text, metadata={"source": url})
        return document, None
    
    except requests.RequestException as e:
        return None, f"Error scraping the website: {str(e)}"

# PDF scraping function
def scrape_pdf(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = " ".join([page.extract_text() or "" for page in pdf.pages])
            text = re.sub(r'\s+', ' ', text).strip()
        
        if not text:
            return None, "No text found in the PDF."
        
        document = Document(page_content=text, metadata={"source": uploaded_file.name})
        return document, None
    
    except Exception as e:
        return None, f"Error processing the PDF: {str(e)}"

# Initialize the chain and template
def initialize_chain(scraped_data):
    template = """
    You are an AI-powered chatbot that only has information from the context provided below.
    If the answer to a question cannot be found in the context, do not guess or provide additional details.
    Instead, respond with: "I'm sorry, I can only provide information based on the scraped content."

    Context: {context}
    Question: {question}
    """
    return scraped_data, template

def web_pdf_chatbot():

    
    st.title("🤖 ScraperBot: Your AI Chat Companion")
    
    st.markdown(
        """
        **Welcome to ScraperBot!**  
        I'm an AI-powered chatbot that answers questions based on content scraped from a website or a PDF you provide. Enter a URL or upload a PDF below, and once the content is processed, you can ask me anything about it!

        ---
        """
    )

    # Initialize session state variables
    if "scraped_data" not in st.session_state:
        st.session_state.scraped_data = None
    if "chain" not in st.session_state:
        st.session_state.chain = None
    if "data" not in st.session_state:
        st.session_state.data = None
    if "template" not in st.session_state:
        st.session_state.template = None
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initialize the Groq chain if not already done
    if "chain" not in st.session_state or st.session_state.chain is None:
        try:
            deepseek, parser, st.session_state.chain = initialize_groq_chain()
        except ValueError as e:
            st.error(str(e))
            return

    # Clear Everything button
    if st.button("Clear Everything"):
        st.session_state.scraped_data = None
        st.session_state.chain = None
        st.session_state.data = None
        st.session_state.template = None
        st.session_state.messages = []
        st.success("Everything has been cleared! Start fresh by scraping a new URL or uploading a PDF.")
        st.rerun()  # Refresh the app to reflect the cleared state

    # Input options: URL or PDF
    st.subheader("Choose Your Input")
    input_option = st.radio("Select input type:", ("Website URL", "PDF Upload"))

    if input_option == "Website URL":
        url = st.text_input("Enter a website URL to scrape (e.g., https://example.com):", "")
        if st.button("Scrape Website") and url:
            with st.spinner("Scraping the website..."):
                scraped_data, error = scrape_website(url)
                if error:
                    st.error(error)
                elif scraped_data:
                    st.session_state.scraped_data = scraped_data
                    st.session_state.data, st.session_state.template = initialize_chain(scraped_data)
                    st.success(f"Successfully scraped content from {url}! You can now ask questions.")
    
    else:  # PDF Upload
        uploaded_file = st.file_uploader("Upload a PDF file:", type=["pdf"])
        if st.button("Process PDF") and uploaded_file:
            with st.spinner("Processing the PDF..."):
                scraped_data, error = scrape_pdf(uploaded_file)
                if error:
                    st.error(error)
                elif scraped_data:
                    st.session_state.scraped_data = scraped_data
                    st.session_state.data, st.session_state.template = initialize_chain(scraped_data)
                    st.success(f"Successfully processed {uploaded_file.name}! You can now ask questions.")

    # Display chat interface only if content has been scraped
    if st.session_state.scraped_data:
        # Display chat history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # Capture user input
        user_input = st.chat_input("Type your question here...")

        if user_input:
            # Append and display user's message
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)

            # Generate AI response
            prompt = st.session_state.template.format(
                context=st.session_state.data.page_content,
                question=user_input
            )
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    raw_answer = st.session_state.chain.invoke(prompt)
                answer_no_think = re.sub(r"<think>.*?</think>", "", raw_answer, flags=re.DOTALL).strip()
                st.write(answer_no_think)

            # Append assistant's response
            st.session_state.messages.append({"role": "assistant", "content": answer_no_think})
    else:
        st.warning("Please provide a URL or upload a PDF and process it before asking questions.")
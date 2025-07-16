import streamlit as st
import google.generativeai as genai
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Helper Functions ---

def load_faq_data(file_path):
    """Loads FAQ data from a JSON file into a pandas DataFrame."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data['questions'])
        return df
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found. Please make sure it's in the same directory as the script.")
        return None
    except (json.JSONDecodeError, KeyError) as e:
        st.error(f"Error reading or parsing the JSON file: {e}")
        return None

def find_most_relevant_question(user_query, faq_df, vectorizer, tfidf_matrix):
    """Finds the most relevant FAQ question for a given user query."""
    if faq_df is None or faq_df.empty:
        return None, None

    # Vectorize the user's query
    query_tfidf = vectorizer.transform([user_query])

    # Calculate cosine similarity between the user query and all FAQ questions
    cosine_similarities = cosine_similarity(query_tfidf, tfidf_matrix).flatten()

    # Get the index of the most similar question
    most_similar_idx = cosine_similarities.argmax()
    
    # Get the similarity score
    highest_similarity_score = cosine_similarities[most_similar_idx]

    # Set a threshold for relevance
    if highest_similarity_score < 0.2: # You can adjust this threshold
        return None, None

    # Return the most relevant question and its answer
    relevant_question = faq_df.iloc[most_similar_idx]
    return relevant_question['question'], relevant_question['answer']

def get_gemini_response(api_key, user_query, context_answer):
    """Gets a conversational response from the Gemini model."""
    try:
        genai.configure(api_key=api_key)
        
        # Create the prompt for the model
        # The prompt guides the model to answer based on the provided context.
        prompt = f"""
        You are a friendly and helpful e-commerce customer support chatbot.
        A customer has asked the following question: "{user_query}"
        
        Use the following information from our FAQ to answer the customer's question:
        "{context_answer}"
        
        If the provided information doesn't directly answer the question, say that you don't have enough information to answer and suggest they contact customer support.
        Keep your answer concise and conversational.
        """
        
        model = genai.GenerativeModel('gemini-2.5-flash') # Using 2.5 Flash as requested
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred with the Gemini API: {e}")
        return "Sorry, I'm having trouble connecting to my brain right now. Please try again later."


# --- Streamlit App ---

st.set_page_config(page_title="E-commerce FAQ Bot", page_icon="🤖")

st.title("🛒 E-commerce Customer Support Chatbot")
st.caption("Powered by Google Gemini & your FAQ data")

# --- API Key and Data Loading ---

# Try to get API key from secrets, fallback to user input
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    st.success("Selamat datang. Saya adalah chatbot yang siap membantu pertanyaan kamu. Silahkan ajukan pertanyaan di kolom chat")
except KeyError:
    st.warning("⚠️ No API key found in secrets. Please enter it below.")
    api_key = st.text_input(
        "Enter your Google API Key", 
        type="password", 
        help="You can get your API key from Google AI Studio."
    )
    
    if not api_key:
        st.info("💡 **Tip**: For better security, add your API key to `.streamlit/secrets.toml`")

# Store API key in session state
if api_key:
    st.session_state.api_key = api_key
else:
    st.session_state.api_key = ''


# Load FAQ data once and store in session state
if 'faq_data' not in st.session_state:
    st.session_state.faq_data = load_faq_data('Ecommerce_FAQ_Chatbot_dataset.json')

faq_df = st.session_state.faq_data

# Initialize TF-IDF Vectorizer if data is loaded
if faq_df is not None and 'vectorizer' not in st.session_state:
    with st.spinner("Analyzing FAQ data..."):
        questions = faq_df['question'].tolist()
        st.session_state.vectorizer = TfidfVectorizer(stop_words='english')
        st.session_state.tfidf_matrix = st.session_state.vectorizer.fit_transform(questions)


# --- Chat Interface ---

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question about our products, shipping, or returns."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Check for API Key and data
    if not st.session_state.api_key:
        with st.chat_message("assistant"):
            st.warning("Please enter your Google API Key above to start the chat.")
        st.stop()
    if faq_df is None:
        with st.chat_message("assistant"):
            st.error("FAQ data could not be loaded. Please check the file and restart.")
        st.stop()

    # --- Generate Response ---
    with st.spinner("Thinking..."):
        # Find the most relevant FAQ
        relevant_q, relevant_a = find_most_relevant_question(
            prompt, 
            faq_df, 
            st.session_state.vectorizer, 
            st.session_state.tfidf_matrix
        )

        if relevant_a:
            # If a relevant answer is found, use Gemini to make it conversational
            response = get_gemini_response(st.session_state.api_key, prompt, relevant_a)
        else:
            # If no relevant context is found
            response = "I'm sorry, I couldn't find a specific answer to your question in our FAQ. For more help, you can contact our customer support team at [email address] or call us at [phone number]."

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

import vertexai
from vertexai.preview.generative_models import GenerativeModel
from google.oauth2 import service_account
import streamlit as st

def initialize_vertex_ai():
    credentials = st.secrets["gcp_service_account"]
    PROJECT_ID = credentials["project_id"]
    REGION = "us-west1"

    creds = service_account.Credentials.from_service_account_info(credentials)
    vertexai.init(project=PROJECT_ID, location=REGION, credentials=creds)

def get_predictions(data):
    initialize_vertex_ai()

    # Convert Dates to strings
    data['Date'] = data['Date'].astype(str)

    # Use the Gemini model for predictions
    generative_multimodal_model = GenerativeModel("gemini-1.5-pro-001")
    
    # Format data for prediction
    instances = data.to_dict(orient='records')

    # Convert data instances to a suitable input for the model
    text_input = str(instances)
    
    # Make predictions
    response = generative_multimodal_model.generate_content(["Generate financial predictions for the following data:", text_input])
    predictions_text = response.text  # Correctly access the text content of the response

    print("Predictions Text:", predictions_text)  # Debugging print

    return predictions_text

def ask_vertex_ai(prompt):
    initialize_vertex_ai()

    # Use the Gemini model for chatbot
    generative_model = GenerativeModel("gemini-1.5-pro-001")
    
    # Make the chatbot request
    response = generative_model.generate_content([prompt])
    chatbot_response = response.text  # Correctly access the text content of the response

    print("Chatbot Response:", chatbot_response)  # Debugging print

    return chatbot_response

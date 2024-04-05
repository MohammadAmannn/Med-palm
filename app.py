import streamlit as st
from pathlib import Path
import google.generativeai as genai

from api_key import api_key  # Make sure you have your API key in a separate file

# Configure Google Generative AI
genai.configure(api_key=api_key)

# Set up the model generation configuration
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Set safety settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

# System prompt (Modify this based on your specific use case)
system_prompt = "Analyze this medical image and provide a detailed diagnosis. Include possible conditions, recommended tests, and treatment options. In sequence point wise give health tips to the user and suggest some medicens also which is not sensitive and second thing you also have to analyse the medical reports like xray ,ECG graph,MRI,CT SCAN report etc "

# Configure GenerativeModel
model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Set page configuration
st.set_page_config(page_title="Med Palm", page_icon="🧑‍⚕️", layout='centered')

# Logo
st.image("we care.png", width=150)

# Title
st.title("Med Palm - Your Medical Assistant")

# Subtitle
st.subheader("How can I help you today?")

# File uploader and button
uploaded_file = st.file_uploader("Upload your medical prescriptions, reports or any other relevant documents.", type=["jpg", "png"])
if uploaded_file:
    st.image(uploaded_file,width=300,caption="Uploaded Image")

submit_button = st.button("Generate the analysis")

if submit_button:
    # Process the uploaded image
    image_data = uploaded_file.getvalue()

    image_parts = [
        {
            "mime_type": "image/jpeg",  # Assuming JPEG format
            "data": image_data
        },
    ]

    prompt_parts = [
        image_parts[0],
        system_prompt,
    ]

    # Generate a response based on prompt and image


    response = model.generate_content(prompt_parts)

    #Display the response with better formatting
    st.markdown("Here is The Analysis Based On Your Image:")  # Add a header 
    st.write(response.text) 

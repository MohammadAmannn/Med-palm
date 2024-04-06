import streamlit as st
from pathlib import Path
import google.generativeai as genai
from streamlit_option_menu  import option_menu

from api_key import api_key  

# Configure Google Generative AI
genai.configure(api_key=api_key)

# Set up the model generation configuration
generation_config = {
    "temperature": 0.7,
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
system_prompt = """""
Analyze this medical image and provide a detailed diagnosis. Include possible conditions, recommended tests, and treatment options. In sequence point wise give health tips to the user and suggest some medicens also which is not sensitive and second thing if a person upload there report you also have to analyse the medical reports  You are A virtual Doctor As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images. 88 Model Gemini Pro Vision Temperature Add stop sequence Your Responsibilities include: Prompt gallery Discand commu 1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings. 
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format. 
 3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments es applicable
 4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.
Important Notes: 
1. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are unable to be determined based on the provided image.

 Disclaimer: Accompany your analysis with the disclaimer: Consult with a Doctor before making any decisions. 4. Your insights are invaluable in guiding clinical if the uploaded prescription is blank and nothing there say please upload a valid report or prescription

 """

#header
st.set_page_config(page_title="Med Palm", page_icon="🧑‍⚕️", layout='centered')

with st.sidebar:
    selected=option_menu(
        menu_title=None,
        options=("Home","About us","Contact Us"),
         icons=["house","info-circle","envelope"]
         
        
    )

    if selected=="Home":
        st.markdown("Welcome to our platform!")
        st.write("This is an AI-powered web application designed for users who want to keep track of there health")
        
        
     
    if selected=="About us":
        st.markdown("We are team We Care And Your Health Is Our Priority")
 
    if selected=="Contact Us": 
     st.write("https://mohammadamannn.github.io/We_Care/")

    

# Configure GenerativeModel
model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


# Logo
st.image("we care.png", width=150)




# Title
st.title("Med Palm - Your Medical Assistant")

# Subtitle
st.subheader("Need  medical advice? Let us help!")

# File uploader and button
uploaded_file = st.file_uploader("Upload your medical prescriptions, reports or any other relevant documents.", type=["jpg", "png","pdf"])
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

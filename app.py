import streamlit as st
import os
import google.generativeai as genai
import data_processing
from PIL import Image, ImageOps
from dotenv import load_dotenv

# Function to generate a response using Google Generative AI
def get_gemini_response(input, image, prompt):
    try:
        response = model.generate_content([input, image[0], prompt])

        # Safely access the candidate text if available
        if response and response.candidates:
            for candidate in response.candidates:
                
                # Access the text within content.parts[0].text
                if candidate.content and candidate.content.parts:
                    return candidate.content.parts[0].text
                else:
                    return "No valid text found in the response content."
        else:
            return "No valid response received. Please check the input or try again."

    except Exception as e:
        return f"An error occurred: {str(e)}"

load_dotenv() # It will load all the environment variables from .env
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="MultiLanguage Invoice Extractor")
st.header("MultiLanguage Invoice Extractor")

input_user = st.text_input("Input Prompt : ", key="input") ## User Input

uploaded_file = st.file_uploader("Choose an image....", type=["jpg", "jpeg", "png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the image")

input_prompt = """
You are an expert in understanding invoices. We will upload a image as invoice and you will have to answer any questions based on the uploaded invoice image.
"""

if submit:
    if uploaded_file:
        image_data = data_processing.input_image_details(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, input_user)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload an image before submitting.")

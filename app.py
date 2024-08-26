import streamlit as st
import os
import google.generativeai as genai
import data_processing
from PIL import Image, ImageOps
from dotenv import load_dotenv

# Creation of Model
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


# Streamlit Webapp Creation
st.set_page_config(page_title="MultiLanguage Invoice Extractor")
st.header("MultiLanguage Invoice Extractor")

input_user = st.text_input("Input Prompt : ", key="input") ## User Input

uploaded_file = st.file_uploader("Choose an image....", type=["jpg", "jpeg", "png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the image")


# Prompt Engineering
input_prompt = """
You are an expert in understanding invoices. We will upload a image as invoice and you will have to answer any questions based on the uploaded invoice image.
"""

# Response Generation
if submit:
    if uploaded_file:
        image_data = data_processing.input_image_details(uploaded_file)
        response = data_processing.get_gemini_response(input_prompt, image_data, input_user, model)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload an image before submitting.")

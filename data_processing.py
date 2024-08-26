import os
from PIL import Image, ImageOps
import io

# Function to handle image preprocessing
def preprocess_image(image, max_size=(1024, 1024)): 
    
    image = image.convert("RGB")# Ensure the image is in RGB mode
    image = ImageOps.contain(image, max_size)# Resize the image while maintaining aspect ratio
    return image


# Function to return image data
def input_image_details(uploaded_file): 
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # Preprocess the image to handle large and diverse image files
        processed_image = preprocess_image(image)
        
        # Convert the processed image to bytes using a byte stream
        img_byte_arr = io.BytesIO()
        processed_image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        image_parts = [{
            "mime_type": "image/jpeg",  # Assuming JPEG format for uniformity
            "data": img_byte_arr
        }]

        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    
# Function to generate a response using Google Generative AI
def get_gemini_response(input, image, prompt, model):
    try:
        response = model.generate_content([input, image[0], prompt])

        # Safely access the candidate text if available
        if response and response.candidates:
            for candidate in response.candidates:    
                
                # Safely access the candidate parts if available
                if candidate.content and candidate.content.parts:
                    return candidate.content.parts[0].text
                else:
                    return "No valid text found in the response content."
        else:
            return "No valid response received. Please check the input or try again."

    except Exception as e:
        return f"An error occurred: {str(e)}"
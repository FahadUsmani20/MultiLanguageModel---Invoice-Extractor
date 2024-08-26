import os
from PIL import Image, ImageOps
import io


def preprocess_image(image, max_size=(1024, 1024)): # Function to handle image preprocessing
    image = image.convert("RGB")# Ensure the image is in RGB mode
    image = ImageOps.contain(image, max_size)# Resize the image while maintaining aspect ratio
    
    return image

def input_image_details(uploaded_file): ## Image Data
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
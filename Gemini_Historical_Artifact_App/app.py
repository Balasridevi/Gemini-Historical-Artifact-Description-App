import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# ==========================================
# MILESTONE 2: Configuration
# ==========================================
# Replace the string below with your actual API key from Google AI Studio
genai.configure(api_key="AIzaSyDjZAenplRFC-ydj133rJ2a947dIrMPvxA")

# ==========================================
# MILESTONE 2.3 & 3: Functions
# ==========================================

def get_gemini_response(input_text, image, prompt):
    """Initializes the model and gets a response."""
    model = genai.GenerativeModel('gemini-2.5-flash')
    # The model expects a list of inputs: [User Text, Image Data, System Prompt]
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    """Processes the uploaded image into bytes for the Gemini API."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# ==========================================
# MILESTONE 4 & 5: UI and Execution
# ==========================================

# Initialize Streamlit App
st.set_page_config(page_title="Gemini Historical Artifact Description App")
st.header("🏺 Gemini Historical Artifact App")

# User inputs
input_prompt = st.text_input("Input Prompt (e.g., 'Describe this'): ", key="input")
uploaded_file = st.file_uploader("Choose an image of an artifact...", type=["jpg", "jpeg", "png"])

# Display image if uploaded
image = ""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image Preview", use_container_width=True)

submit = st.button("Generate Artifact Description")

# The specific System Prompt for the AI
system_instruction = """
You are a historian. Please describe the historical artifact in the image 
and provide detailed information, including its name, origin, time period, 
and historical significance.
"""

# Logic to run when button is clicked
if submit:
    if uploaded_file is not None:
        with st.spinner("Analyzing artifact..."):
            try:
                # Prepare image data
                image_data = input_image_setup(uploaded_file)
                
                # Get response from Gemini
                response = get_gemini_response(input_prompt, image_data, system_instruction)
                
                # Output
                st.subheader("Description of the Artifact:")
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload an image first!")
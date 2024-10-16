import streamlit as st
from PIL import Image
import pytesseract
from gtts import gTTS
import os

# Set the path for Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Streamlit UI styling
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
    }
    .stButton > button {
        background-color: #6c63ff;
        color: white;
        border-radius: 12px;
        font-size: 16px;
        padding: 8px 12px;
        margin-top: 10px;
    }
    .stButton > button:hover {
        background-color: #4832d3;
    }
    .stTextInput {
        border: 1px solid #ddd;
        padding: 8px;
        border-radius: 10px;
    }
    .stDownloadButton > button {
        background-color: #28a745;
        color: white;
        border-radius: 12px;
        font-size: 16px;
        padding: 8px 12px;
        margin-top: 10px;
    }
    .stDownloadButton > button:hover {
        background-color: #218838;
    }
    h1 {
        color: #6c63ff;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📷 Text Recognition and Audio Generator Using Python and Streamlit 🎵")

st.write("Upload an image to extract text, convert it to audio, and download the results!")

# Sidebar instructions
st.sidebar.title("How to Use:")
st.sidebar.write("""
1. Upload an image containing text.
2. Extract the text.
3. Convert the extracted text to an audio file.
4. Download the text or audio.
""")

# File uploader for the image
uploaded_file = st.file_uploader("🖼️ Choose an image file...", type=["png", "jpg", "jpeg"])

# If an image is uploaded
if uploaded_file is not None:
    # Load and display the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True, channels="RGB")

    # Perform OCR using pytesseract
    st.write("🔍 **Extracting Text from Image...**")
    try:
        text = pytesseract.image_to_string(image)
        
        if text.strip():
            st.success("Text successfully extracted!")
            st.text_area("📜 Extracted Text (for copy):", text, height=150)
            
            # Provide options to download the text as a file
            st.download_button(
                label="💾 Download Extracted Text",
                data=text,
                file_name="extracted_text.txt",
                mime="text/plain"
            )

            # Text-to-speech conversion using gTTS
            if st.button("🎤 Convert Text to Audio"):
                tts = gTTS(text=text, lang='en')
                tts.save("extracted_audio.mp3")
                audio_file = open("extracted_audio.mp3", "rb").read()

                # Provide an option to download the audio file
                st.audio(audio_file, format="audio/mp3")
                st.download_button(
                    label="🔊 Download Audio",
                    data=audio_file,
                    file_name="extracted_audio.mp3",
                    mime="audio/mp3"
                )
        else:
            st.error("No text could be extracted from the image. Please try another image.")
    except pytesseract.pytesseract.TesseractNotFoundError:
        st.error("Tesseract OCR not found. Please ensure it is installed and the path is set correctly.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    st.info("👈 Upload an image file from your Device to get started.")

# Footer with contact details
st.markdown("""
    ---
    Made by Gude Venkata Mohana Krishna
""")

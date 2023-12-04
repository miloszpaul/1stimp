import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
from PIL import Image
import numpy as np
import tempfile
import zoom

# Set up the logo, title, and introduction of the app
st.image("images/logo.png", width=150)
st.title('First Impression for Videocalls')
st.write('This application provides insights into your first impression in videocalls based on the uploaded image or live camera feed.')

# Image Upload or Camera Feed Section
option = st.radio("Choose input method:", ("Upload Image", "Use Camera"))

if option == "Upload Image":
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Your Uploaded Image', use_column_width=True)

        # Save the uploaded image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            image.save(tmp_file)
            tmp_file_name = tmp_file.name

        # Process the image using zoom.py
        results = zoom.process_image(tmp_file_name)
        st.write(results)

elif option == "Use Camera":
    class VideoProcessor(VideoTransformerBase):
        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")

            # Save the frame to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                cv2.imwrite(tmp_file.name, img)
                tmp_file_name = tmp_file.name

            # Process the image using zoom.py
            results = zoom.process_image(tmp_file_name)
            st.write(results)
            return frame

    webrtc_ctx = webrtc_streamer(key="example", video_processor_factory=VideoProcessor)

# Additional Guidelines (if needed)
st.subheader('Guidelines')
st.image("images/background.png", width=350)
st.write('Here are some guidelines for selecting appropriate images for analysis...')

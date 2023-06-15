import os
import streamlit as st
import requests
import cv2
import numpy as np
from PIL import Image
import io
import json
import openai
import time
from pathlib import Path
import base64
from diseases import disease_info
from test import loading_message, validate_result, chat_with_chatgpt

#load variables
BASE_URI = st.secrets['cloud_api_uri']
url = BASE_URI + '/predict'
OPENAI_API_KEY=st.secrets['OPENAI_API_KEY']

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css?family=Comfortaa&display=swap');
html, body [class*="css"] {
    font-family: 'Comfortaa', sans-serif;
    font-size: 20px !important;
    font-weight: 200;
    color: #091747;
    }

.stProgress > div > div > div > div {
            background-color: #40916C;
        }
}
</style>
""", unsafe_allow_html=True)


logo = Image.open('media/LeafScan-logos.png')
st.image(logo)

uploaded_files = st.file_uploader(label="Upload your leaf picture :four_leaf_clover:", accept_multiple_files=True, type=['jpg','jpeg','png','gif'])

chat_check= st.checkbox('Do you want ChatGPT indications if your plants are sick ? :ambulance: ')
submit = st.button('Launch the scan')
if submit:
    if uploaded_files is not None:

        for upld in uploaded_files:
            i = 0
            image = Image.open(upld)
            #left_co, cent_co,last_co = st.columns(3)
            #with cent_co:
            st.image(image, caption=f'Your uploaded leaf', width=400)
            if image.format == "PNG":
                image = image.convert("RGB")
            # convert the PIL image to byte array
            image_bytes = io.BytesIO()

            with st.spinner('Loading your photo...'):
                image.save(image_bytes, format="JPEG")
                image_bytes = image_bytes.getvalue()


            with st.spinner('Sending your photo...'):
                response = requests.post(url, files={'img': image_bytes})

                st.write('Starting the prediction process.')
                # Assuming the API responds with JSON

                if response.status_code == 200:
                    api_result = (response.json())
                    loading_message()
                    st.write(validate_result(api_result[i]))

                    if not list(api_result[i].keys())[0].endswith('ealthy') and not (list(api_result[i].keys())[0].endswith('eaves')):
                        prompt ='What are the 3 main actions to do against ' + list(api_result[i].keys())[0] + ' disease(s)'
                        repGPT = chat_with_chatgpt(prompt)

                        container = st.container()
                        with container:
                            if chat_check :
                                st.write("Asking chatGPT: " + prompt)
                                st.write(repGPT)


                            else:
                                st.write("Failed to send the image to the API.")
            i += 1

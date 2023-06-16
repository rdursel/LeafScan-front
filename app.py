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
    font-size: 26px;
    font-weight: 300;
    color: #091747;
    }

.css-10trblm  {
            font-size: 80 px !important;
            font-weight: bold;
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

submit = st.button('Launch the scan')
if submit:
    if uploaded_files is not None:

        for upld in uploaded_files:
            i = 0
            image = Image.open(upld)
            #left_co, cent_co,last_co = st.columns(3)
            #with cent_co:
            st.image(image, width=400)
            # st.image(image, caption=f'Your uploaded leaf', width=400)
            if image.format == "PNG":
                image = image.convert("RGB")
            # convert the PIL image to byte array
            image_bytes = io.BytesIO()

            with st.spinner('Loading your photo...'):
                image.save(image_bytes, format="JPEG")
                image_bytes = image_bytes.getvalue()


            with st.spinner('Sending your photo...'):
                response = requests.post(url, files={'img': image_bytes})

            # st.write('Starting the prediction process.')
            # Assuming the API responds with JSON

            if response.status_code == 200:
                api_result = (response.json())
                loading_message()
                col1, col2, col3 = st.columns([1, 3, 1])
                with col2:
                    st.write("<br>", unsafe_allow_html=True)
                    st.markdown(f'# {validate_result(api_result[i])}')
                st.write("<br><br>", unsafe_allow_html=True)
                st.text(" ")
                st.text(" ")

                if not list(api_result[i].keys())[0].endswith('ealthy') and not (list(api_result[i].keys())[0].endswith('eaves')):
                    prompt ='What are the 3 main actions to do against ' + list(api_result[i].keys())[0] + ' disease(s)'
                    repGPT = chat_with_chatgpt(prompt)

                    container = st.container()
                    with container:
                        st.markdown("**Advice:**")
                        st.write(repGPT)

            else:
                st.write("Failed to send the image to the API.")
            i += 1

#Final test
with st.expander( 'About us', expanded=False):
    st.write('''

We are an innovative plant leaf detection application designed to swiftly identify plant diseases using leaf images. Our advanced machine learning and computer vision algorithms enable us to quickly detect diseases and determine the specific plant species.

Features:

    Tomato
    Raspberry
    Grapes
    Apple
    Cherry
    Corn
    Potato
    Soybean
    Bell Pepper
    Strawberry
    Orange
    Peach
    Blueberry
    Squash


Our mission is to assist gardening enthusiasts, farmers, and plant lovers in making informed decisions and protecting their crops from diseases. Download our plant leaf detection application today and confidently care for your plants!

Note: Please be aware that our application is intended for informational and preliminary diagnostic purposes only. For accurate diagnoses and specific treatments, we recommend consulting an agricultural or horticultural expert.''')

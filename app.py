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


#load variables
BASE_URI = st.secrets['cloud_api_uri']
url = BASE_URI + '/predict'
OPENAI_API_KEY=st.secrets['OPENAI_API_KEY']

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def validate_result(api_result,threshold=70):
    '''
    This function ensure a minimal score and print result
    '''
    first_category = list(api_result.keys())[0]
    secund_category = list(api_result.keys())[1]
    third_category = list(api_result.keys())[2]
    first_value_accuracy = round(list(api_result.values())[0]*100,2)
    if first_category == 'Background without leaves':
        return "Sorry, no leaf detected.  Please try again."
    if first_category.endswith('ealthy') and first_value_accuracy > threshold :
        return "Sure at "+ str(first_value_accuracy) + "% that I've detected a " + f' **{first_category}** '
    if first_value_accuracy > threshold :
         return "Sure at "+ str(first_value_accuracy) + "% that I've detected a " + f' **{first_category}** : ' + f' disease infos here 👉[link]({disease_info(first_category)})' + "!"
    else:
         return "I'm hesitating between "+ first_category + ", " + secund_category + " and " + third_category+". Please try again."


def chat_with_chatgpt(prompt, model="text-davinci-003"):
    '''
    send a prompt to chatGPT api.  Reply with a str()
    '''
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message


def loading_message():
    '''
    This function display a progress bar with custom messages
    '''
    message_list = [
            '## Loading image',
            '## Guillaume is finetuning the model ... :dna:',
            '## Guillaume is finetuning the model ... :dna:',
            '## Raphaël is checking if the prediction makes sense...:passport_control:',
            '## Raphaël is checking if the prediction makes sense...:passport_control:',
            '## Alice is looking into a dictionary about the detected disease... :leaves:',
            '## Alice is looking into a dictionary about the detected disease... :leaves:',
            '## Open a ticket.. :admission_tickets:',
            '## Open a ticket.. :admission_tickets:',
            '## Trust the process 	:sunglasses:',
            '## DONE ! :white_check_mark:'
        ]


    my_bar = st.progress(0, text=message_list[0])

    for percent_complete in range(1,100):
        time.sleep(0.07)
        message_id=int(percent_complete/len(message_list)+1)
        my_bar.progress(percent_complete + 1, text=message_list[message_id])
    return None

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

if uploaded_files is not None:

       for upld in uploaded_files:
           i=0
           image = Image.open(upld)
           left_co, cent_co,last_co = st.columns(3)
           with cent_co:
               st.image(image, caption=f'Your uploaded leaf', width=400)

           if image.format == "PNG":
            image = image.convert("RGB")
           # convert the PIL image to byte array
           image_bytes = io.BytesIO()

           with st.spinner('Loading your photo...'):
                image.save(image_bytes, format="JPEG")
                image_bytes = image_bytes.getvalue()


           with st.spinner('Loading your photo...'):
                response = requests.post(url, files={'img': image_bytes})

           st.write('Starting the prediction process.')
           # Assuming the API responds with JSON
           if response.status_code == 200:
               api_result = (response.json())
               loading_message()
               st.write(validate_result(api_result[i]))

               if not list(api_result[i].keys())[0].endswith('ealthy') and not (list(api_result[i].keys())[0].endswith('eaves')):
                   ask_chatGPT = st.checkbox("chatGPT help me to treat this disease, please :ambulance:")
                   if ask_chatGPT:
                    prompt ='What are the 3 main actions to do against ' + list(api_result[i].keys())[0] + ' disease(s)'
                    st.write('Asking to chatGPT : '+prompt )
                    st.write( chat_with_chatgpt(prompt))
           else:
               st.write("Failed to send the image to the API.")
           i=+1

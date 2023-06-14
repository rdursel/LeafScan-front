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
        return "I'm sorry, I'm not able to recognize the leaf, could you feed me with another image please?"
    if first_value_accuracy > threshold:
         return "Yes! I'm fairly sure, at "+ str(first_value_accuracy) + "% that I've detected a " + first_category + "!"
    else:
         return "MmmmmmH... I'm not quite confident. \
                I'm hesitating between "+ first_category + ", " + secund_category + " and " + third_category+". \
                Would you have another image to help me out?"


def chat_with_chatgpt(prompt, model="text-davinci-003"):
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
            'Setting up the API url to:  '+url,
            'The image is sent to API...',
            'The image is rescaled to 256x256 pixels...',
            'The image is being rotated randomly to create augmented features...',
            'The image is now ready to be analyzed...',
            'Guillaume is finetuning the model :)',
            'Raphaël is checking if the prediction makes sense...',
            'Alice is looking into a dictionary about the detected disease...',
            'Getting back the 3 mains probabilities from the API',
            'Be patient, it \' coming.... :)',
            'DONE !'
        ]

    my_bar = st.progress(0, text=message_list[0])

    for percent_complete in range(1,100):
        time.sleep(0.1)
        message_id=int(percent_complete/len(message_list)+1)
        my_bar.progress(percent_complete + 1, text=message_list[message_id])
    return None

# #Afficher le fond vert pâle à l'aide de st.markdown()
# st.markdown(green_background, unsafe_allow_html=True)

left_column, right_column = st.columns(2)

# Côté gauche (Drag and Drop)
#with left_column:

# Titre en vert
header_html = f"""
            <h1 style='text-align: center; text-color:#081C15'>
                LeafScan App
                <img
                    src='data:image/png;base64,{
                        img_to_bytes(
                            "media/icons/001-leaf.png"
                            )}'
                    class='img-fluid'>
            </h1>
                """
st.markdown(
    header_html, unsafe_allow_html=True,
)
st.markdown('<style>h1{font-size: 50px;}</style>', unsafe_allow_html=True)
# Section Drag and Drop
st.header('Drag and Drop')

uploaded_files = st.file_uploader("Choose image files", accept_multiple_files=True, type=None)
ask_chatGPT = st.checkbox("I'd like to receive chatGPT advices to treat the detected disease (if any)")

# Côté droit (Prédictions et images)
#with right_column:

# Titre des prédictions
st.header('Predictions')
if uploaded_files is not None:

       for upld in uploaded_files:
           i=0

           image = Image.open(upld)
           st.image(image, caption=f'Uploaded Image ({image.format}).', width=200)
           if image.format == "PNG":
            image = image.convert("RGB")
           # convert the PIL image to byte array
           image_bytes = io.BytesIO()
           image.save(image_bytes, format="JPEG")
           image_bytes = image_bytes.getvalue()

           # Use 'rb' if you get an error about 'bytes-like object is required, not str'
           response = requests.post(url, files={'img': image_bytes})

           # Assuming the API responds with JSON
           if response.status_code == 200:
               api_result = (response.json())
               loading_message()
               st.write(validate_result(api_result[i]))
               if ask_chatGPT:
                   prompt ='What are the 3 main actions to do against ' + list(api_result[i].keys())[0] + ' disease(s)'
                   st.write('Asking to chatGPT : '+prompt )
                   st.write( chat_with_chatgpt(prompt))
           else:
               st.write("Failed to send the image to the API.")
           i=+1

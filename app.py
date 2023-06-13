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



# Define the base URI of the API
#   - Potential sources are in `.streamlit/secrets.toml` or in the Secrets section
#     on Streamlit Cloud
#   - The source selected is based on the shell variable passend when launching streamlit
#     (shortcuts are included in Makefile). By default it takes the cloud API url
if 'API_URI' in os.environ:
    BASE_URI = st.secrets[os.environ.get('API_URI')]
else:
    BASE_URI = st.secrets['cloud_api_uri']
# Add a '/' at the end if it's not there
BASE_URI = BASE_URI if BASE_URI.endswith('/') else BASE_URI + '/'
# Define the url to be used by requests.get to get a prediction (adapt if needed)

url = BASE_URI + 'predict'
OPENAI_API_KEY=st.secrets['OPENAI_API_KEY']

# Just displaying the source for the API. Remove this in your final version.
st.markdown(f"Working with {url}")
st.markdown("Now, the rest is up to you. Start creating your page.")


def validate_result(api_result,threshold=0.7):
    '''
    This function ensure a minimal score
    '''
    if round(api_result[0]['accuracy'],2) < threshold:
        return False
    else:
        return True

def chat_with_chatgpt(prompt, model="text-davinci-003"):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message


def loading_message():
   message_list = [
        'The image is sent to API...',
        'The image is now rescaled',
        'The image is now rotated randomly',
        'The image is ready to be analyzed...',
        'Alice is looking into a dictionary about the detected disease',
        'Guillaume is doing his best to...',
        'Getting back the 3 mains probabilities'
        '...nearly done.  Be patient ;)'
    ]

   my_bar = st.progress(0,text=message_list[0])

   for i, message in enumerate(message_list):
        my_bar.text(message)
        time.sleep(0.1)
        my_bar.progress((i + 1) * 100 // len(message_list))

   return None




uploaded_file = st.file_uploader("Choose a image file", type=['jpg'], accept_multiple_files=True)
ask_chatGPT = st.checkbox("I'd like to receive chatGPT advice")

if uploaded_file is not None:
    for upld in uploaded_file:
        image = Image.open(upld)
        st.image(image, caption='Uploaded Image.', width=200)

        # convert the PIL image to byte array
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes = image_bytes.getvalue()

        #st.write("Sending image to the API...")

        # Use 'rb' if you get an error about 'bytes-like object is required, not str'
        response = requests.post(url, files={'img': image_bytes})

        # Assuming the API responds with JSON
        if response.status_code == 200:
            loading_message()
            #st.write("Successfully sent to the API!")
            st.write(response.json())
            #st.write(response.json()[0])
            #data = json.load(response.json())
            #print(data)
            st.write("3 main probabilites are : ")
            for lm in range(len(response.json())):
                for k, v in response.json()[lm].items():
                    #print( k, v)
                    if ask_chatGPT:
                        st.write('Asking to chatGPT : what are the 3 main actions to do against ' + k )
                        st.write( chat_with_chatgpt("what are the 3 main actions to do against " + k+" disease ?"))


        else:
            st.write("Failed to send the image to the API.")

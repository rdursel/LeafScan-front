import os
import streamlit as st
import requests
import cv2
import numpy as np
from PIL import Image
import io

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

# Just displaying the source for the API. Remove this in your final version.
st.markdown(f"Working with {url}")

st.markdown("Now, the rest is up to you. Start creating your page.")



uploaded_file = st.file_uploader("Choose a image file", type="jpg")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

     # convert the PIL image to byte array
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes = image_bytes.getvalue()

    st.write("Sending image to the API...")

    # Use 'rb' if you get an error about 'bytes-like object is required, not str'
    response = requests.post(url, files={'img': image_bytes})

    # Assuming the API responds with JSON
    if response.status_code == 200:
        st.write("Successfully sent to the API!")
        st.write(response.json())
    else:
        st.write("Failed to send the image to the API.")


# TODO: Add some titles, introduction, ...


# TODO: Request user input


# TODO: Call the API using the user's input
#   - url is already defined above
#   - create a params dict based on the user's input
#   - finally call your API using the requests package


# TODO: retrieve the results
#   - add a little check if you got an ok response (status code 200) or something else
#   - retrieve the prediction from the JSON


# TODO: display the prediction in some fancy way to the user



# TODO: [OPTIONAL] maybe you can add some other pages?
#   - some statistical data you collected in graphs
#   - description of your product
#   - a 'Who are we?'-page

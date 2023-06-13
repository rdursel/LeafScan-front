import os
import streamlit as st
import requests
import cv2
import numpy as np
from PIL import Image
import io

green_background = """
<style>
body {
    background-color: lightgreen;
}
</style>
"""
# Afficher le fond vert pâle à l'aide de st.markdown()
st.markdown(green_background, unsafe_allow_html=True)



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
left_column, right_column = st.columns(2)

# Côté gauche (Drag and Drop)
with left_column:
    # Titre en vert
    st.title('LeafScan')
    st.markdown('<style>h1{color: green;}</style>', unsafe_allow_html=True)
    # Section Drag and Drop
    st.header('Drag and Drop')

    uploaded_files = st.file_uploader("Choose image files", accept_multiple_files=True, type="jpg")

    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            st.write("File:", uploaded_file.name)

# Côté droit (Prédictions et images)
with right_column:
    # Titre des prédictions
    st.header('Predictions')

    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image.', use_column_width=True)

            # Convertir l'image PIL en tableau d'octets
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='JPEG')
            image_bytes = image_bytes.getvalue()

            st.write("Sending image to the API...")

            # Utiliser 'rb' si vous obtenez une erreur indiquant 'bytes-like object is required, not str'
            response = requests.post(url, files={'img': image_bytes})

            # Supposant que l'API répond avec JSON
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

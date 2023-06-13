import streamlit as st
import requests
from datetime import datetime

# Titre en vert
st.title('LeafScan')
st.markdown('<style>h1{color: green;}</style>', unsafe_allow_html=True)
# Section Drag and Drop
st.header('Drag and Drop')
uploaded_files = st.file_uploader('Déposer les fichiers ici', accept_multiple_files=True)
# Bouton "Upload from Local Files"
st.header('Upload from Local Files')
file_path = st.text_input('Chemin du fichier')
# Bouton "Predict"
if st.button('Predict'):
    # Logique de prédiction à implémenter ici
    st.write('Prédiction en cours...')
    # Résultats de la prédiction
    st.success('Prédiction terminée!')

if __name__ == '__main__':
    main()

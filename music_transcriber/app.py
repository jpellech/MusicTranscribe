import streamlit as st
import os
from werkzeug.utils import secure_filename
from MusicAssist import process_music  # Import the main function from MusicAssist.py

# Set up upload and output folders
upload_folder = 'inputs'
output_folder = 'output'
os.makedirs(upload_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# Streamlit App
st.title("Music Transcriber")
st.subheader("Upload an audio file to transcribe it into instrument-separated MIDI and .mp3 files.")

uploaded_file = st.file_uploader("Choose an audio file", type=['wav', 'mp3', 'mp4', 'flac'])
st.write("")
st.subheader("Usage tips:")
st.write("Drag the MIDI files into any musical notation software to learn one or more parts from sheet music.")
st.write("Or drag the MIDI into your digital audio workstation and change the sounds.")
st.write("Use the isolated .mp3s to sample certain parts of songs.")

if uploaded_file is not None:
    # Save uploaded file
    filename = secure_filename(uploaded_file.name)
    file_path = os.path.join(upload_folder, filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File {filename} uploaded successfully.")

    try:
        # Call the process_music function from MusicAssist.py
        result = process_music(file_path)
        st.success('File processed successfully.')
        st.text(result)
    except Exception as e:
        st.error(f'Error processing file: {e}')

    # Check if the output folder exists and contains the expected zip file
    zip_filename = f"{os.path.splitext(filename)[0]}.zip"
    zip_filepath = os.path.join(output_folder, zip_filename)
    
    if os.path.exists(zip_filepath):
        with open(zip_filepath, 'rb') as f:
            st.download_button('Download processed files', f, file_name=zip_filename)
    else:
        st.error(f"Zip file not found: {zip_filepath}")

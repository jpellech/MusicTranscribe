import streamlit as st
import subprocess
import os
from werkzeug.utils import secure_filename

# Set up upload folder
upload_folder = 'inputs'
output_folder = 'output'
os.makedirs(upload_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# Streamlit App
st.title("Music Transcriber")
st.subheader("Upload an audio file to transcribe it into instrument-separated MIDI and .wav files.")

uploaded_file = st.file_uploader("Choose an audio file", type=['wav', 'mp3', 'mp4', 'flac'])
st.write("")
st.subheader("Usage tips:")
st.write("Drag the midi files into any Musical Notation software to learn one or more parts from sheet music.")
st.write("Or drag the midi into your Digital Audio Workstation and change the sounds.")
st.write("Use the isolated .mp3s to sample certain parts of songs.")

if uploaded_file is not None:
    # Save uploaded file
    filename = secure_filename(uploaded_file.name)
    file_path = os.path.join(upload_folder, filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File {filename} uploaded successfully.")

    # Assuming 'python' is the correct interpreter with all dependencies installed
    command = ["python", "music_transcriber/MusicAssist.py", file_path]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        st.success('File processed successfully.')
        st.text(result.stdout)
    except subprocess.CalledProcessError as e:
        st.error(f'Error processing file: {e}')
        st.text(e.stderr)

    # Check if the output folder exists and contains the expected zip file
    zip_filename = f"{os.path.splitext(filename)[0]}.zip"
    zip_filepath = os.path.join(output_folder, zip_filename)
    
    if os.path.exists(zip_filepath):
        with open(zip_filepath, 'rb') as f:
            st.download_button('Download processed files', f, file_name=zip_filename)
    else:
        st.error(f"Zip file not found: {zip_filepath}")

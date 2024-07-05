from flask import Flask, render_template, request, send_from_directory
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='static/templates')

current_path = os.path.abspath(__file__)
directory_path = os.path.dirname(current_path)
output_folder = os.path.join(directory_path, "output")

app.config['STATIC_FOLDER'] = os.path.join(directory_path, 'static')
app.config['STATIC_URL_PATH'] = '/static'
app.config['UPLOAD_FOLDER'] = os.path.join(directory_path, 'inputs')

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def index():
    return render_template('index.html')

app.add_url_rule('/', 'index', index)

@app.route('/process_file', methods=['POST'])
def process_file():
    # Check if a file is attached to the POST request
    if 'file' not in request.files:
        return "No file uploaded.", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file.", 400
    
    # Secure the filename and save the file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Run MusicAssist.py with the file path
    command = ["poetry", "run", "python3", os.path.join(directory_path, "MusicAssist.py"), file_path]
    print('COMMAND:', ' '.join(command))
    try:
        subprocess.run(command)
        print('subprocess is done. returning zip now . . . ')
    except:
        print('Unsuccesful run.')

    # Check if the output folder exists
    if os.path.exists(output_folder):
        zip_filename = f"{os.path.splitext(filename)[0]}.zip"
        zip_filepath = os.path.join(output_folder, zip_filename)
        
        if os.path.exists(zip_filepath):
            # Prepare the zip file for download
            return send_from_directory(output_folder, zip_filename, as_attachment=True)
        else:
            return f"Zip file not found: {zip_filepath}", 404
    else:
        return f"Output folder not found: {output_folder}", 404
def install_poetry():
    subprocess.run(["curl", "-sSL", "https://install.python-poetry.org", "|", "python3", "-"], check=True)
    os.environ["PATH"] += os.pathsep + os.path.expanduser("~/.local/bin")

def check_and_install_spleeter():
    try:
        subprocess.run(["poetry", "run", "spleeter", "-h"], check=True)
    except subprocess.CalledProcessError:
        print("Installing Spleeter...")
        subprocess.run(["poetry", "add", "spleeter"])
        subprocess.run(["poetry", "install"])

if __name__ == '__main__':
    install_poetry()
    check_and_install_spleeter()
    app.run(debug=True)
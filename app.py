import os
from flask import Flask, request, render_template, redirect, send_file, send_from_directory
import cv2
from scanner import scan_and_warp

app = Flask(__name__)

UPLOAD_FOLDER = 'static/images/uploads'
DOCUMENT_FOLDER = 'static/images/documents'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOCUMENT_FOLDER'] = DOCUMENT_FOLDER

# Create the upload and document directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOCUMENT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return "No image selected"
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            return render_template('index.html', uploaded_image=filename.replace('\\', '/'))
        else:
            return "Invalid file format"

@app.route('/remove', methods=['POST'])
def remove_file():
    action = request.form['action']
    if action == 'remove':
        uploaded_image = request.form['uploaded_image']
        os.remove(uploaded_image)
    return redirect('/')

@app.route('/scan', methods=['GET', 'POST'])
def scan_file():
    action = request.form['action']
    if action == 'scan':
        uploaded_image = request.form['uploaded_image']
        try:
            scanned_document = scan_and_warp(uploaded_image)
            if scanned_document is not None:
                filename = os.path.basename(uploaded_image)
                scanned_document_path = os.path.join(app.config['DOCUMENT_FOLDER'], filename)
                cv2.imwrite(scanned_document_path, scanned_document)
                return redirect('/document?scanned_image_path=' + scanned_document_path.replace('\\', '/'))
            else:
                return "Sorry, couldn't find any document in the uploaded image. Please upload an image of better quality."
        except Exception as e:
            # raise e
            return "An error occurred during scanning. Please upload an image of better quality."



@app.route('/document')
def document():
    scanned_image_path = request.args.get('scanned_image_path')
    filename = os.path.basename(scanned_image_path)
    return render_template('document.html', scanned_image_path=scanned_image_path, filename=filename)

@app.route('/download')
def download():
    scanned_image_path = request.args.get('scanned_image_path')
    return send_file(scanned_image_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

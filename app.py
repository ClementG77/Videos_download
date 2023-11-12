from flask import Flask, render_template, redirect, flash, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
from utils import *
import os, subprocess


UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/script', methods=['POST'])
def upload_video():
    
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No video selected for uploading')
        return redirect(request.url)
    else:
        part_duration = request.form.get('duration')
        output_folder = 'static/output/'
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        command = f'python cut.py static/uploads/{filename} {output_folder} {part_duration}'
        subprocess.run(command, shell=True)
        videos = get_videos()
        print(videos)
                
        return render_template('result.html' , len=len(videos), videos=videos)

@app.route('/display/<filename>')
def display_video(filename):
    #print('display_video filename: ' + filename)
    return redirect(url_for('static', filename='output/' + filename), code=301)

def get_videos():
    videos = []
    for filename in os.listdir('static/output'):
         f = os.path.join('static/output', filename)
         videos.append(f)
    
    return videos



if __name__ == "__main__":
    # Quick test configuration. Please use proper Flask configuration options
    # in production settings, and use a separate file or environment variables
    # to manage the secret key!
    
    app.run()
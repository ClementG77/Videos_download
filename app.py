from flask import Flask, render_template, redirect, flash, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
from utils import *
import os, subprocess, shutil, pathlib,re


UPLOAD_FOLDER = 'static/uploads/'
OUTPUT_FOLDER = 'static/output/'

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def home():
    reset_folder(OUTPUT_FOLDER)
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
        videos = get_videos('static/output')
                
        return render_template('result.html' , len=len(videos), videos=videos)

@app.route('/display/<filename>')
def display_video(filename):
    #print('display_video filename: ' + filename)
    return redirect(url_for('static', filename='output/' + filename), code=301)

def get_videos(path):
    videos = []
    for filename in os.listdir(path):
         f = os.path.join(path, filename)
         videos.append(f)
    
    return videos

def reset_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))





@app.route('/resize',methods=['GET', 'POST'])
def resize_video():
    
    filename = request.args.get("filename")

    filename = filename.replace("%2F","/")
    filename = filename.replace("%5C","/")
    
    path = "static/resize"
    pathl = pathlib.Path(filename)
    output = f"resized_{pathl.name}"
    command = f'python resize.py {filename} {path} {output} '
    subprocess.run(command, shell=True)
    # file = request.files['button']
    # part_duration = request.form.get('duration')
    # output_folder = 'static/output/'
    # filename = secure_filename(file.filename)
    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # 
    # 
    # videos = get_videos()
                
    return render_template('comeback.html')


if __name__ == "__main__":
    # Quick test configuration. Please use proper Flask configuration options
    # in production settings, and use a separate file or environment variables
    # to manage the secret key!
    
    app.run(debug=True)
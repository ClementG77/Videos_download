from flask import Flask, render_template, redirect, flash, request, send_from_directory, url_for, session
from werkzeug.utils import secure_filename
from utils import *
import os, subprocess, shutil, pathlib,re
from threading import Timer
import webbrowser
from flask_socketio import SocketIO


UPLOAD_FOLDER = 'static/uploads/'
OUTPUT_FOLDER = 'static/output/'
RESIZE_FOLDER = 'static/resize/'
ROTATE_FOLDER = 'static/rotate/'
DOWNLOAD_FOLDER = 'static/download'

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def home():
    reset_folder(OUTPUT_FOLDER)
    return render_template('home.html')
@app.route('/rd')
def resetDownload():
    reset_folder(DOWNLOAD_FOLDER)
    return render_template('home.html')
@app.route('/rr')
def resetResize():
    reset_folder(RESIZE_FOLDER)
    return render_template('home.html')
@app.route('/rT')
def resetRotate():
    reset_folder(ROTATE_FOLDER)
    return render_template('home.html')
@app.route('/rU')
def resetUpload():
    reset_folder(UPLOAD_FOLDER)
    return render_template('home.html')



@app.route('/cutPage')
def cutPage():
    return render_template("cut.html")

@app.route('/script', methods=['POST'])
def upload_video():
    url = request.form.get('url')
    output_name = request.form.get('output_name')
    part_duration = request.form.get('duration')
    print(output_name)
    if url != "":
        if 'youtube' in url :
            path = DOWNLOAD_FOLDER
            output_name = request.form.get('output_name') + ".mp4"
            command = f'python yt_download.py {url} {path} {output_name}'
            subprocess.call(command, shell=True)
        else:
            path = DOWNLOAD_FOLDER
            url = '"' + url +'"'
            command = f'python videoDownloader.py {url} {output_name}'
            print(command)
            subprocess.call(command, shell=True)
            videos = [f for f in os.listdir() if '.mp4' in f.lower()]

            for video in videos:
                new_path = 'static/download/' + video
                shutil.move(video, new_path)
            output_name = output_name+"HD.mp4"
        
        output_folder = 'static/output/'
        command = f'python cut.py static/download/{output_name} {output_folder} {part_duration}'
        subprocess.run(command, shell=True)
        
        videos = get_videos('static/output')
        return render_template('result.html' , len=len(videos), videos=videos)
    
    file = request.files['file']
    if file.filename == '':
        flash('No video selected for uploading')
        return redirect(request.url)
    else:
        output_folder = 'static/output/'
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        session['file'] = 'static/uploads/'+filename
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




@app.route('/resizePage')
def resizePage():
    return render_template("resize.html")

@app.route('/resizePreview')
def resizePreview():
    filename = request.args.get("filename")
    command = f'python preview.py {filename}'
    subprocess.run(command, shell=True)
    return redirect(url_for('reupload_video',file=filename, resized=False))

@app.route('/resize',methods=['GET', 'POST'])
def resize_video():
    
    filename = request.args.get("filename")

    filename = filename.replace("%2F","/")
    filename = filename.replace("%5C","/")
    
    file = session.get('file')
    file_parts = os.path.splitext(filename)[0].split('_')  # Split the filename and remove the extension
    part_number = file_parts[1][4:] 
    session['number'] = part_number


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
                
    return redirect(url_for('reupload_video',file= file,resized=True,number = part_number))

@app.route('/rotatePage')
def rotatePage():
    return render_template("rotate.html")

@app.route('/rotatePreview')
def rotatePreview():
    filename = request.args.get("filename")
    command = f'python rotatePreview.py {filename}'
    subprocess.run(command, shell=True)
    return redirect(url_for('reupload_video',file=filename, resized=False))

@app.route('/rotate',methods=['GET', 'POST'])
def rotate_video():
    filename = request.args.get("filename")

    filename = filename.replace("%2F","/")
    filename = filename.replace("%5C","/")


    pathl = pathlib.Path(filename)
    output = f"static/rotate/rotated_{pathl.name}"
    command = f'python rotate.py {filename} {output} '
    subprocess.run(command, shell=True)
                
    return redirect(url_for('reupload_video',file=filename,resized=True))



@app.route('/rerender', methods=['POST',"GET"])
def reupload_video():
    number = request.args.get('number')
    resized = request.args.get('resized')
    
    file = request.args.get("file")
    file = file.replace("%2F","/")
    file = file.replace("%5C","/")

    if file == '':
        flash('No video selected for uploading')
        return redirect(request.url)
    else:
        videos = get_videos('static/output')
                
        return render_template('result.html' , len=len(videos), videos=videos , resized= resized, number=number)


@app.route('/customPage')
def customPage():
    return render_template("custom.html")


def open_browser():
      webbrowser.open_new("http://127.0.0.1:5000")



if __name__ == "__main__":
    # Quick test configuration. Please use proper Flask configuration options
    # in production settings, and use a separate file or environment variables
    # to manage the secret key!
    Timer(1, open_browser).start()
    app.run(debug=True)
from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename
import pytube
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from SVMFinal import extract_feature
import time
import ssl
import urllib.request
import tempfile
import io


app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
app.config['ALLOWED_EXTENSIONS'] = {'.wav', '.mp3', '.aif'}


ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
ssl._create_default_https_context = ssl._create_unverified_context



@app.route('/')
def main():
    return render_template('main.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method =='POST':
        file = request.files['music-file']  # This is the file NAME in the HTML

        if file:
            filename = secure_filename(file.filename)
            extension = os.path.splitext(filename)[1].lower()
            if extension not in app.config['ALLOWED_EXTENSIONS']:
                message = 'Error: This is not an mp3, wav, or aif...'
            else:
                response = extract_feature(os.path.join('uploads', filename))

                message = ''
        else:
            message = 'Error: There was no file submitted...'

        return render_template('main.html', message=message, response=response)
    else:
        pass
    
    
@app.route('/youtube_upload', methods=['POST'])
def youtube_upload():   
    if request.method == 'POST':
        # try:
        youtube_link = request.form.get('youtube-link')  # Access the value of the 'youtube-link' input field
        if youtube_link:
        
            yt = pytube.YouTube(youtube_link)
            stream = yt.streams.filter(only_audio=True).first()
            filename = secure_filename(''.join(list(stream.default_filename)[0:-4]) + '.wav')
           
            stream.download(filename=filename)
            
            response = extract_feature(filename)
            
            try:
                os.remove(filename)  
            except:
                pass

        else:
            return render_template('main.html')

        return render_template('main.html', response=response)

if __name__ == '__main__':
    app.run(port=8083, debug=True)


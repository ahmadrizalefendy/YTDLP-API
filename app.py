from flask import Flask, request, jsonify, send_from_directory, render_template
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
URL = 'YOUR DOMAIN URL'

# Index page
@app.route('/')
def home():
    return render_template('index.html')

# Audio Download Here
@app.route('/audio', methods=['GET'])
def download_audio():
    url = request.args.get('url')
    name = request.args.get('name')

    if not url and not name:
        return jsonify({'error': 'Either URL or name is required'}), 400

    if name:
        search_query = f"ytsearch:{name}"
    else:
        search_query = url

    ydl_opts = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
        'cookiefile': 'cookies.txt', # Missed a comma here
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(search_query, download=True)
            title = info_dict.get('title', 'unknown')
            file_path = ydl.prepare_filename(info_dict)
            output_filename = secure_filename(f"{uuid.uuid4()}.mp3")
            output_path = os.path.join(DOWNLOAD_FOLDER, output_filename)

            # Convert to MP3 using pydub
            audio = AudioSegment.from_file(file_path)
            audio.export(output_path, format="mp3", bitrate="192k")

            # Clean up temporary files
            if os.path.exists(file_path):
                os.remove(file_path)

        return jsonify({
            'download_url': f'{URL}/download/{output_filename}',
            'name': title,
            'url': url or search_query
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Video Download Here
@app.route('/video', methods=['GET'])
def download_video():
    url = request.args.get('url')
    name = request.args.get('name')

    if not url and not name:
        return jsonify({'error': 'Either URL or name is required'}), 400

    if name:
        search_query = f"ytsearch:{name}"
    else:
        search_query = url

    ydl_opts = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
        'cookiefile': 'cookies.txt', # Missed a comma here
        'format': 'bestvideo[height<=360]+bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(search_query, download=True)
            title = info_dict.get('title', 'unknown')
            file_path = ydl.prepare_filename(info_dict)
            output_filename = secure_filename(f"{uuid.uuid4()}.mp4")
            output_path = os.path.join(DOWNLOAD_FOLDER, output_filename)

            # Rename file to have .mp4 extension
            os.rename(file_path, output_path)

        return jsonify({
            'download_url': f'{URL}/download/{output_filename}',
            'name': title,
            'url': url or search_query
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Download Link Function Here
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
    app.run(host='0.0.0.0', port=5000)

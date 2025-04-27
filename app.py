from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
import browser_cookie3
import yt_dlp
import sys

app = Flask(__name__)
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def get_ydl_opts(url):
    return {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
        'cookiefile': 'cookies.txt',
        'format': 'best',
        'nocheckcertificate': True,  # Ignore SSL certificate checks
        'no_cookie': True,  # Ignore cookies entirely
        'no_warnings': True  # Disable warnings
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "❌ Error: No URL provided."

    try:
        if "threads.net" in url or "threads.com" in url:
            return "❌ Error: Threads downloading is currently not supported. Stay tuned! 🚀"

        ydl_opts = get_ydl_opts(url)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)

        final_filename = os.path.basename(filename)
        return redirect(url_for('downloads', filename=final_filename))

    except Exception as e:
        return f"❌ Error during download: {str(e)}"

@app.route('/downloads/<filename>')
def downloads(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
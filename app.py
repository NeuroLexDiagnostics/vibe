import os
import random

from flask import (
    Flask,
    render_template,
    request,
    Response,
)
from werkzeug.middleware.shared_data import SharedDataMiddleware


def get_random_folder():
    listdir = os.listdir()
    folders = list()
    for i in range(len(listdir)):
        if listdir[i].find('.') < 0:
            folders.append(listdir[i])
    return random.choice(folders)


def get_giphy():
    listdir = os.listdir()
    for i in range(len(listdir)):
        if listdir[i].endswith('.mp4'):
            return listdir[i]


# set some helper functions
def allowed_file(filename):
    return filename.endswith('.wav')


# def video_feed():
# return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# configuration steps for Flask
# load the model 
# set some defaults 
app = Flask(__name__, template_folder='templates', static_folder='static')

curdir = os.getcwd()
app.config['BASE_FOLDER'] = curdir
app.config['UPLOAD_FOLDER'] = curdir + '/upload'
app.config['PROCESSED_FOLDER'] = curdir + '/published'
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024 * 2
curdir = os.getcwd()


app.add_url_rule('/published/<filename>', 'uploaded_file', build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/published': app.config['PROCESSED_FOLDER'],
})

os.makedirs('upload', exist_ok=True)
os.makedirs('published', exist_ok=True)

# camera = cv2.VideoCapture(0)
'''
for ip camera use - rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' 
for local webcam use cv2.VideoCapture(0)
'''


@app.route('/', methods=['GET'])
def serve_front():
    base_url = request.base_url
    return render_template('index.html', url=base_url)


@app.route('/templates', methods=['GET'])
def templates():
    base_url = request.base_url.replace('/templates', '')
    return render_template('templates.html', url=base_url)


@app.route('/record', methods=['GET'])
def record_audio():
    base_url = request.base_url.replace('/record', '')
    return render_template('record.html', base_url=base_url)


@app.route('/picture', methods=['GET'])
def picture():
    base_url = request.base_url
    return render_template('picture.html', base_url=base_url)


@app.route('/video', methods=['GET'])
def video():
    base_url = request.base_url
    return render_template('video.html', base_url=base_url)


@app.route('/sentence', methods=['GET'])
def sentence():
    base_url = request.base_url
    return render_template('sentence.html', base_url=base_url)


@app.route('/calibration', methods=['GET'])
def calibration():
    # base_url = request.base_url
    return render_template('calibration.html')


@app.route('/video_feed', methods=['GET'])
def video_feed():
    base_url = request.base_url
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000, ssl_context=('adhoc'))

from flask import Flask, render_template, request

from audio_recoder import AudioRecorder

app = Flask(__name__)


@app.route(rule="/")
def index_page():
    return "Audio recording page"


@app.route(rule="/start", methods=['POST'])
def start_record():
    request_ = request.get_json()
    podcast_name = request_['filename']
    AudioRecorder(audio_file_name=podcast_name).start()


@app.route(rule="/stop", methods=['POST'])
def stop_record():
    request_ = request.get_json()
    podcast_name = request_['filename']
    AudioRecorder(audio_file_name=podcast_name).stop()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

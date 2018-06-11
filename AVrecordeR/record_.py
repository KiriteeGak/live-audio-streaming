from flask import Flask, render_template

from AVrecordeR.audio_recoder import start_recording, stop_recording

app = Flask(__name__)


@app.route(rule="/")
def index_page():
    return "Audio recording page"


@app.route(rule="/start", methods=['POST'])
def start_record():
    start_recording()


@app.route(rule="/stop", methods=['POST'])
def stop_record():
    stop_recording()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

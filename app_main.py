from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
from gevent import monkey

from audio_recoder import AudioRecorder

# monkey.patch_all()

app = Flask(__name__)

reference_dict = dict()


@app.route(rule="/")
def index_page():
    return "Welcome to live audio streaming"


@app.route(rule="/audio/<type_>", methods=['GET', 'POST'])
def start_record(type_):
    request_ = request.get_json()
    recording_name = request_['filename']
    try:
        if type_ == 'start':
            cls_ = AudioRecorder(audio_file_name=recording_name)
            reference_dict[recording_name] = cls_
            cls_.record()
            return jsonify({"message": "Recording successfully started"})
        elif type_ == 'stop':
            cls_ = reference_dict[recording_name]
            cls_.stop()
            return jsonify({"message": "Recording successfully stopped"})
        else:
            return jsonify({"message": "Unable to process get request"})
    except KeyError:
        return jsonify({"message": "Unable to find the class object to stop the instance"})


@app.route(rule="/seek", methods=['POST'])
def seek_record():
    # request_ = request.get_json()
    # recording_name = request_['filename']
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, processes=1)
    # http_ = WSGIServer(('', 5000), app.wsgi_app)
    # http_.serve_forever()

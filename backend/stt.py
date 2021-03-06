from tempfile import NamedTemporaryFile
import json
from flask import request
from speech_recognition import Recognizer, AudioFile

from backend import app, API_VERSION, USE_DEEPSPEECH
from backend.decorators import noindex, requires_auth

recognizer = Recognizer()

if USE_DEEPSPEECH:
    from extra.deepspeech_stt import DeepSpeechSTT

    engine = DeepSpeechSTT()
    recognize = engine.recognize
else:
    recognize = recognizer.recognize_google


@app.route("/" + API_VERSION + "/stt", methods=['POST'])
@noindex
@requires_auth
def stt():
    flac_audio = request.data
    lang = str(request.args.get("lang", "en-us"))
    with NamedTemporaryFile() as fp:
        fp.write(flac_audio)
        with AudioFile(fp.name) as source:
            audio = recognizer.record(source)  # read the entire audio file

        utterance = recognize(audio, language=lang)
    return json.dumps([utterance])

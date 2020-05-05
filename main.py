import urllib.request
import json
import base64
import subprocess
import time
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

import text_analyzer

FOLDER_ID = ""
IAM_TOKEN = ""
RAW_AUDIO_FOLDER = "./audios/webm/"
NORMALIZED_AUDIO_FOLDER = "./audios/ogg/"

app = Flask(__name__)
CORS(app)

def timestamp():
    return str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"))

def write_raw_received_audio(audio_b64, timestamp):
    data = base64.b64decode(audio_b64)
    filepath = RAW_AUDIO_FOLDER + timestamp + ".webm"
    f = open(filepath, "wb")
    f.write(data)
    f.close()
    return filepath
    
def normalize_audio(raw_audio_path, timestamp):
    filepath = NORMALIZED_AUDIO_FOLDER + timestamp + ".ogg"
    command = "ffmpeg -i " + raw_audio_path + " -ab 160k -ac 2 -ar 44100 -vn " + filepath
    subprocess.call(command, shell=True)
    return filepath
    
@app.route('/recognize', methods=['POST'])
def recognize_audio():
    content = request.json
    
    ts = timestamp()
    fpath = write_raw_received_audio(content['audio'], ts)
    fpath = normalize_audio(fpath, ts)
    
    f = open(fpath, mode='rb')
    audio = f.read()
    f.close()
    
    params = "&".join([
        "topic=general",
        "folderId=%s" % FOLDER_ID,
        "lang=ru-RU"
    ])
    url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=audio)
    url.add_header("Authorization", "Bearer %s" % IAM_TOKEN)

    responseData = urllib.request.urlopen(url).read().decode('UTF-8')
    decodedData = json.loads(responseData)
    
    if decodedData.get("error_code") is None:   
        result_message =  decodedData.get("result")
        print(result_message)
        return jsonify({"message":result_message})
    
@app.route('/analyze', methods=['POST'])
def analyze_speach_text():
    content = request.json
    text = content["message"]
    print(text)
    result = text_analyzer.analyze(text)
    s = 0
    for word, score in result.items():
        text = text.replace(word, "<mark>"+word+"</mark>")
        s += score
    critical = False
    if s > 0.7:
        critical = True
    return jsonify({"scores":result, "critical": critical, "text": text})

if __name__ == "__main__":
    FOLDER_ID = os.environ['FOLDER_ID']
    IAM_TOKEN = os.environ['IAM_TOKEN']
    
    os.makedirs(RAW_AUDIO_FOLDER, exist_ok=True)
    os.makedirs(NORMALIZED_AUDIO_FOLDER, exist_ok=True)

    print("Folder id: ", FOLDER_ID)
    print("I am token: ", IAM_TOKEN)
    
    app.run(host= '127.0.0.1', port='8888',debug=True)

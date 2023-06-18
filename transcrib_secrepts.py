import os
import time
import whisper
import requests

from api_secrepts import API_KEY_ASSEMBLY


def transcribing_ASSEMBLY(file_path):
    base_url = "https://api.assemblyai.com/v2"

    # up-lode
    headers = {
        "authorization": API_KEY_ASSEMBLY
    }
    with open(file_path, "rb") as f:
        response = requests.post(base_url + "/upload",
                                 headers=headers,
                                 data=f)

    upload_url = response.json()["upload_url"]

    # transcribe
    data = {
        "audio_url": upload_url
    }
    url = base_url + "/transcript"
    response = requests.post(url, json=data, headers=headers)

    # polling
    transcript_id = response.json()['id']
    polling_endpoint = f"{base_url}/transcript/{transcript_id}"

    while True:
        transcription_result = requests.get(polling_endpoint, headers=headers).json()

        if transcription_result['status'] == 'completed':
            os.remove(file_path)
            return transcription_result, None

        elif transcription_result['status'] == 'error':
            raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

        else:
            time.sleep(2)


def transcribing_whisper(filename):
    model = whisper.load_model("small")
    result = model.transcribe(filename, fp16=False)
    os.remove(filename)
    return result

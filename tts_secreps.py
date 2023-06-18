import time
import pygame
import urllib.parse
import requests
import os

from api_secrepts import API_KEY_XILABS


def voicevox_speck(jp_txt, specker_id):

    timestamp = str(time.time()).replace(".", "")
    speech_filename = f"\\tts_audio\\tts_jp_{timestamp}.wav"
    os.makedirs(os.path.dirname(speech_filename), exist_ok=True)
    voicevox_url = "http://127.0.0.1:50021"

    # Posting_audio_query
    text = jp_txt
    speaker = specker_id

    # Prepare the request payload
    payload = {
        "text": text,
        "speaker": speaker
    }
    encod = urllib.parse.urlencode(payload)

    # Send the POST request
    response = requests.post(f"{voicevox_url}/audio_query?{encod}", json=payload)

    # Check the response status code
    if response.status_code == 200:
        # Successful response
        audio_query = response.json()  # Get the JSON response data
        # Process the audio_query as needed
    else:
        # Error response
        error_message = response.json()["detail"]
        print(f"Request failed: {error_message}")

    # posting_synthesis

    audio_query["prePhonemeLength"] = 1.0
    audio_query["postPhonemeLength"] = 1.0
    audio_query["volumeScale"] = 2.0
    audio_query["intonationScale"] = 1.5
    encod = urllib.parse.urlencode({'speaker': speaker, 'enable_interrogative_upspeak': True})

    # Send the POST request
    response = requests.post(f'{voicevox_url}/synthesis?{encod}', json=audio_query)

    # Check the response status code
    if response.status_code == 200:
        outfile = open(speech_filename, "wb")
        outfile.write(response.content)
        outfile.close()
        # playing audio
        playsound(speech_filename)
    else:
        # Error response
        error_message = response.json()["detail"]
        print(f"Request failed: {error_message}")


def elevenLab_speck(txt, specker_id):
    timestamp = str(time.time()).replace(".", "")
    speech_filename = f"/tts_xi_{timestamp}.wav"

    xi_api = API_KEY_XILABS
    voice = specker_id

    CHUNK_SIZE = 1024
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": xi_api
    }

    data = {
        "text": txt,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, json=data, headers=headers)
    # Check the response status code
    if response.status_code == 200:
        # Successful response
        with open(speech_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        # playing audio
        playsound(speech_filename)
    else:
        # Error response
        error_message = response.json()
        print(f"Request failed: {error_message}")


def playsound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

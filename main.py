import pyaudio
import wave
import keyboard

from transcrib_secrepts import *
from tts_secreps import *
from translate_secreps import *
from api_secrepts import XILABS_VOICEID

recorded_filename = 'recorded_audio.wav'


def run():
    while True:
        record_audio()
        text = transcribing_call()
        if text == " Stop.":
            break
        text = translater_call(text)
        speck_call(text)


def record_audio():
    input("Press Enter to start recording...")

    CHUNK = 3200
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    print("Press shift key to stop recording...")
    print("Recording...")

    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        print(".", end="", flush=True)
        if keyboard.is_pressed('shift'):
            break

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(recorded_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"Audio recorded and saved as '{recorded_filename}'.")


def transcribing_call():
    # transcribing -> ASSEMBLY AI
    # data, error = transcribing_ASSEMBLY(recorded_filename)
    # text = data['text']
    # if data:
    #     print(f"Transcribed audio : {text}")
    #     text_file = "transcribed_audio.txt"
    #     with open(text_file, "w") as f:
    #         f.write(text)
    # elif error:
    #     print("ERROR!!!", error)

    # transcribing -> whisper
    transcribed_data = transcribing_whisper(recorded_filename)
    text = transcribed_data['text']
    print(f"Transcribed audio : {text}")
    text_file = "transcribed_text.txt"
    try:
        with open(text_file, "w") as f:
            f.write(text)
        return text
    except:
        return "ERROR!!!"


def translater_call(txt):
    # translating -> googletrans
    translated_data = translate_english_to_japanese(txt)
    trn_text = translated_data.text
    print(f"JA : {trn_text}")
    return trn_text


def speck_call(txt):
    xi_id = XILABS_VOICEID
    vv_id = 66
    voicevox_speck(txt, vv_id)
    # elevenLab_speck(txt, xi_id)


if __name__ == '__main__':
    run()

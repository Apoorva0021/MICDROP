import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

q = queue.Queue()

model_path = "models/vosk-model-small-en-us-0.15"
model = Model(model_path)

def callback(indata, frames, time, status):
    q.put(bytes(indata))

with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    rec = KaldiRecognizer(model, 16000)
    print(" Speak into your mic...")

    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print("You said:", result.get("text"))

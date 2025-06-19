import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
import time

q = queue.Queue()

#for this part please refer the README.md file :)
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
        start_time = time.time()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print("You said:", result.get("text"))
            print("The response time is : ",round(end_time - start_time , 2), "seconds\n") 
            #here the response time was actually very fast like 0.02 seconds , 0.04 seconds.
 

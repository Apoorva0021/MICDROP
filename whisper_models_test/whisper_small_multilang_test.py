
import whisper
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

model = whisper.load_model("small")  # You can try "base" later too

# Change this path to your actual full path for the audio file
audio_path = r"C:\Users\JK TECH\Documents\audio_test_file\multilang_audio_test.m4a"

start = time.time()
result = model.transcribe(audio_path)
end = time.time()

print("\nTranscription by whisper small model")
print(result["text"])
print(f"\n Time taken by whisper small model: {round(end - start, 2)} seconds")

import whisper
import time
from jiwer import wer

model = whisper.load_model("small")  


audio_path = r"C:\Users\JK TECH\Documents\audio_test_file\long_test.m4a"

start = time.time()
result = model.transcribe(audio_path)
output_text = result["text"]
end = time.time()

reference_text_in_audio = "This app helps turn spoken words into written text even when you are offline. it's made to help students and anyone who wants to save ideas quickly by just speaking."

print("\n Transcription by whisper small model:")
print(result["text"])
print("")

print('refrence text : ')
print(reference_text_in_audio)

print("\n Word Error Rate(WER) by whisper small model: ")
print("WER :", wer(reference_text_in_audio , output_text ))
print(f"\n Time taken by whisper small model: {round(end - start, 2)} seconds")
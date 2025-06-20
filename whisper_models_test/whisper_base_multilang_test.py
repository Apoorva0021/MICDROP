import whisper
import time
from jiwer import wer

model = whisper.load_model("base")  


audio_path = r"C:\Users\JK TECH\Documents\audio_test_file\multilang_audio_test.m4a"

start = time.time()
result = model.transcribe(audio_path)
output_text = result["text"]
end = time.time()

reference_text_in_audio = '''English, This speech to text project will help students to record their ideas quickly and accurately.
 Hindi, yeh project chatron ko apni baatein jaldi aur shi treeke se record karne mein madad karega.
   Code mixed , yeh project unke liye h jo apne ideas jaldi aur clearly record karna chahte hain.  '''

print("\n Transcription by whisper base model:")
print(result["text"])
print("")

print('refrence text : ')
print(reference_text_in_audio)

print("\n Word Error Rate(WER) by whisper base model: ")
print("WER :", wer(reference_text_in_audio , output_text ))
print(f"\n Time taken by whisper base model: {round(end - start, 2)} seconds")
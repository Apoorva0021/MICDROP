Hey! 
This folder is part of my work for testing whisper models in STT project.
Here i have uploded diffrent python test files to evaluate how well whispher models convert speech to tezt,
using 3 versions
1) tiny
2) base
3) small
for testing larger models(like whisper large v3)' i used Hugging face online platform instead of running them locally on my laptop to avoid memory and performence issues.\
i uploaded my own audio file there on their hosted space and used their transcription feature to evaluate the model performance.

in the uploaded code files you will get a test for both
1) english only
2) mixed language (eng + hindi)

AUDIO PATH:
actually you will need to change it to your own audio filepath if you want to test.

WHAT YOU WILL NEED:
pip install git+https://github.com/openai/whisper.git
pip install torch
pip install ffmpeg-python
pip install jiwer

thats it..

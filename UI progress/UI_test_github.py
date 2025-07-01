# here we are importing all required libraries
import streamlit as st # to build web app UI
import whisper # whisper model for audio transcription
import os # help to work with file path
import time # by this we will calculate trancription time
import queue # this is for handling real time audio queue
import sounddevice as sd # help capture audio from mic
import json # it will handle json result from vosk
from vosk import Model, KaldiRecognizer # vosk model for live speech transcription
import random # by this we will show random quotes from given list in our web
from PIL import Image #this will help to show the logo in webapp


# Set ups:
st.set_page_config(page_title="Voicova", layout="wide")


logo_path = "logo.jpeg" 

if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    # this will help to show app name and logo name side by side
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(logo, width=100)
    with col2:
        st.markdown("<h1 style='margin-bottom: 0;'>Voicova</h1>", unsafe_allow_html=True)
        st.markdown("<p style='margin-top: 0; color: gray;'>Speak, we will write it down</p>", unsafe_allow_html=True)
else:
    st.warning("Logo image not found. Please make sure 'logo.jpeg' is in the same folder as your script.")




# quotes
quotes = [
    "Your voice matters. Let it be heard.",
    "From thoughts to words — beautifully transcribed.",
    "Every great idea starts with a single word.",
    "Speak with ease. We'll take care of the rest.",
    "Say it. We script it.",
    "Transforming speech into powerful stories."
]

st.markdown(f"<p style='text-align:center; color:gray; font-style:italic;'>{random.choice(quotes)}</p>", unsafe_allow_html=True)



# Sticky Note-style Top Goal of the day with teset button
with st.container():
    if "goal_entered" not in st.session_state:
        st.session_state.goal_entered = False
    if "user_goal" not in st.session_state:
        st.session_state.user_goal = ""

    if not st.session_state.goal_entered:
        st.markdown("""
            <div style="background-color: #CBC3E3; border-radius: 12px; padding: 20px; width: 70%; max-width: 500px; margin: auto; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
                <h4 style="text-align:center; margin-top:0; color: black;">📝 Top Goal of the Day</h4>
            </div>
        """, unsafe_allow_html=True)

        user_input = st.text_input(" ", placeholder="Write your goal here (e.g., Complete EDC notes ✅)")
        if user_input:
            st.session_state.user_goal = user_input
            st.session_state.goal_entered = True

    else:
        st.markdown(f"""
            <div style="background-color: #fffde7; border-radius: 8px; padding: 20px; width: 100%; max-width: 500px; margin: auto; box-shadow: 1px 1px 5px rgba(0,0,0,0.1); color: #333;">
                <b>Your Goal:</b><br>{st.session_state.user_goal}
            </div>
        """, unsafe_allow_html=True)

        if st.button("Reset Goal"):
            st.session_state.goal_entered = False
            st.session_state.user_goal = ""



# here we ask user to choose the model according to their need..
option = st.radio("Choose your method:", ("Whisper (upload audio)", "Vosk (live speech)"))


# ------------------------ WHISPER SECTION ------------------------
if option == "Whisper (upload audio)":
    @st.cache_resource
    def load_whisper_model():
        return whisper.load_model("small")

    model = load_whisper_model()

    audio_file = st.file_uploader("Upload an audio file (.mp3, .wav, .m4a)", type=["mp3", "wav", "m4a"])

    if audio_file is not None:
        st.audio(audio_file)
        with st.spinner("Transcribing... please wait"):
            with open("temp_audio.m4a", "wb") as f:
                f.write(audio_file.read())

            start_time = time.time()
            result = model.transcribe("temp_audio.m4a")
            end_time = time.time()

        st.success(f"Transcription completed in {round(end_time - start_time, 2)} seconds.")
        st.subheader("Transcribed Text:")
        st.write(result["text"])

    # if user want to download the transcribe text so here are the download options
    download_option = st.selectbox("Download as:", ("None", "Text (.txt)", "PDF (.pdf)"))

    if download_option == "Text (.txt)":
        st.download_button(
            label="Download TXT",
            data=result["text"],
            file_name="transcription.txt",
            mime="text/plain"
        )

    elif download_option == "PDF (.pdf)":
        from fpdf import FPDF

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in result["text"].split("\n"):
            pdf.multi_cell(0, 10, line)
        pdf_output = pdf.output(dest='S').encode('latin1')

        st.download_button(
            label="Download PDF",
            data=pdf_output,
            file_name="transcription.pdf",
            mime="application/pdf"
        )


# ------------------------ VOSK SECTION ------------------------
elif option == "Vosk (live speech)":
    st.info("This uses your microphone to record and transcribe in real time.")

#providing path to the vosk model
    vosk_model_path = "vosk-model-small-en-us-0.15" 
    if not os.path.exists(vosk_model_path):
        st.error("Vosk model not found. Please download and extract it first.")
    else:
        model = Model(vosk_model_path)
        rec = KaldiRecognizer(model, 16000)
        q = queue.Queue()

        def callback(indata, frames, time_, status):
            q.put(bytes(indata))

# here also user choose option according to..what they want(only transcribtion or want to create a checklist)
        st.write("Select your mode:")
        mode = st.radio("Choose Functionality:", ("Live Transcription", "Checklist Mode"))

        start_button = st.button("Start Listening")

        if start_button:
            st.write("Speak now...")

            with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                                   channels=1, callback=callback):
                result_text = ""
                checklist_items = []

                for _ in range(100): 
                    data = q.get()
                    if rec.AcceptWaveform(data):
                        res = json.loads(rec.Result())
                        text = res.get("text", "")
                        if text:
                            if mode == "Checklist Mode":
                                checklist_items.append(text)
                            else:
                                result_text += text + " "

            
            st.empty()

            if mode == "Checklist Mode":
                st.subheader("Checklist:")
                for i, item in enumerate(checklist_items):
                    st.checkbox(item, key=f"chk_{i}")
            else:
                st.subheader("Live Transcription:")
                st.write(result_text)
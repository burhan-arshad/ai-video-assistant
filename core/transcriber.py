import whisper
import os

model_name = os.getenv("WHISPER_MODEL", "small")
_model=None

def load_model():
    global _model
    if _model is None:
        print(f"Loading Whisper model: {model_name}")
        _model=whisper.load_model(model_name)
        print("Model loaded successfully.")
    return _model

def transcribe_audio(audio_path:str, translate:bool=False)->str:
    model=load_model()
    task="translate" if translate else "transcribe"
    result=model.transcribe(audio_path, task=task)
    return result["text"]

def transcribe_all(audio_chunks:list, translate:bool=False):
    full_transcription=""
    for i, chunk in enumerate(audio_chunks):
        print(f"Transcribing chunk {i + 1}")
        text=transcribe_audio(chunk, translate)
        full_transcription+=text+" "

    return full_transcription.strip()

import whisper

def transcribe_audio(audio_path):
    model = whisper.load_model("small")  # Use 'base', 'small', or 'large' model
    result = model.transcribe(audio_path)
    return result["text"]

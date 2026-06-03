#-------------------->
#REQUIRED LIBRARIES
#-------------------->
import whisper
import os
import requests
from pydub import AudioSegment

#-------------------->
#LOADING SARVAM MODEL
#-------------------->
SARVAM_PIECE_SECONDS = 25
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_STT_TRANSLATE_URL = "https://api.sarvam.ai/speech-to-text-translate"
SARVAM_MODEL = os.getenv("SARVAM_STT_MODEL", "saaras:v2.5")

#-------------------->
'''
CREATE A FUNCTION TO 
LOAD WHISPER MODEL TO
YOUR PC LOCALLY
'''
#-------------------->
import streamlit as st

@st.cache_resource
def load_model():
    print('Loading whisper model...')
    return whisper.load_model('small')

#-------------------->
'''
CREATE A FUNCTION TO
TRANSCRIBE CHUNKS INTO
TEXT FORM
'''
#-------------------->
def transcribe_chunk_whisper(chunk_path: str) -> str:
    model = load_model()
    result = model.transcribe(chunk_path, task="transcribe")
    return result["text"]

#-------------------->
'''
WRITE A FUNCTION TO 
TRANSCRIBE A CHUNK
USING SARVAM
'''
#-------------------->
def _send_to_sarvam(piece_path: str) -> str:
    """Send one ≤30s WAV file to Sarvam and return the English transcript."""
    headers = {"api-subscription-key": SARVAM_API_KEY}

    with open(piece_path, "rb") as f:
        files = {"file": (os.path.basename(piece_path), f, "audio/wav")}
        data = {"model": SARVAM_MODEL, "with_diarization": "false"}
        response = requests.post(
            SARVAM_STT_TRANSLATE_URL,
            headers=headers,
            files=files,
            data=data,
            timeout=120,
        )

    if not response.ok:
        print(f"\n❌ Sarvam returned {response.status_code}")
        print(f"Response body: {response.text}\n")
        response.raise_for_status()

    return response.json().get("transcript", "")

#-------------------->
'''
WRITE A FUNCTION TO 
CONVERT LONG FILES
INTO SMALL CHUNKS 
'''
#-------------------->
def transcribe_chunk_sarvam(chunk_path: str) -> str:
    """
    Sarvam sync API only accepts ≤30s audio. We split this chunk into
    25-second pieces, send each separately, and join the transcripts.
    """
    if not SARVAM_API_KEY:
        raise RuntimeError("SARVAM_API_KEY is not set in environment / .env")

    audio = AudioSegment.from_wav(chunk_path)
    piece_ms = SARVAM_PIECE_SECONDS * 1000

    full_text = ""
    total_pieces = (len(audio) + piece_ms - 1) // piece_ms

    for i, start in enumerate(range(0, len(audio), piece_ms)):
        piece = audio[start: start + piece_ms]
        piece_path = f"{chunk_path}_sv_{i}.wav"
        piece.export(piece_path, format="wav")

        try:
            print(f"  → Sarvam piece {i + 1}/{total_pieces} ...")
            full_text += _send_to_sarvam(piece_path) + " "
        finally:
            if os.path.exists(piece_path):
                os.remove(piece_path)

    return full_text.strip()

#-------------------->
'''
WRITE A FUNCTION TO CALL 
THE MODEL DEPENDING ON
THE LANGUAGE PROVIDED BY
THE USER
SARVAM -> HINGLISH
WHISPER -> ENGLISH
'''
#-------------------->
def transcribe_chunk(chunk_path: str, language: str = "english") -> str:
    if language.lower() == "hinglish":
        return transcribe_chunk_sarvam(chunk_path)
    return transcribe_chunk_whisper(chunk_path)

#-------------------->
'''
WRITE A FINAL FUNCTION
TO TRANSCRIBE ALL THE 
CHUNKS ONE BY ONE
'''
#-------------------->
def transcribe_all(chunks: list, language: str = "english") -> str:
    full_transcript = ""

    engine = "Sarvam AI" if language.lower() == "hinglish" else "Whisper"
    print(f"Using {engine} for transcription.")

    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i + 1}/{len(chunks)}...")
        text = transcribe_chunk(chunk, language=language)
        full_transcript += text + " "

    print("Transcription complete.")
    return full_transcript.strip()

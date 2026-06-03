#-------------------->
#REQUIRED LIBRARIES
#-------------------->
import yt_dlp
from pydub import AudioSegment
import os

#-------------------->
#CREATING DIRECTORIES
#-------------------->
DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

#-------------------->
''' 
CODE TO DOWNLOAD AND
EXTRACT META DATA OF 
A YOUTUBE VIDEO USING
yt_dlp LIBRARY
'''
#-------------------->
def download_youtube_audio(url: str) -> str:
    # Use a safe output template to avoid potential space or character issues
    output_path = os.path.join(DOWNLOAD_DIR, '%(id)s.%(ext)s')

    ydl_opts = {
        # Fallback format: tries best audio, falls back to ANY available audio
        "format": "ba/b",
        "outtmpl": output_path,
        # Ignore minor extraction errors to allow fallback formats to download
        "ignoreerrors": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        # Temporarily turning off quiet helps us debug if it still fails
        "quiet": False,
    }

    # FIX: Only add cookiefile if it actually exists (crashes on Streamlit Cloud otherwise)
    if os.path.exists("cookies.txt"):
        ydl_opts["cookiefile"] = "cookies.txt"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract metadata and download
        info = ydl.extract_info(url, download=True)

        # FIX: Handle case where info is None due to ignoreerrors=True
        if info is None:
            raise RuntimeError(f"yt_dlp could not extract info for URL: {url}")

        # FIX: Handle playlists — get the first entry if it's a playlist
        if 'entries' in info:
            info = info['entries'][0]

        # Safely determine the final downloaded .wav path
        video_id = info.get('id', url.split("v=")[-1].split("&")[0])
        filename = os.path.join(DOWNLOAD_DIR, f"{video_id}.wav")

    # FIX: Verify the file actually exists before returning
    if not os.path.exists(filename):
        raise FileNotFoundError(
            f"Download seemed to succeed but file not found at: {filename}"
        )

    return filename

#-------------------->
'''
FUNCTION TO CONVERT ANY
AUDIO/VIDEO FILE TO WAV
EXTENSION.
'''
#-------------------->
def convert_to_wav(input_path: str) -> str:
    output_path = os.path.splitext(input_path)[0] + '_converted.wav'
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)  # 16khz
    audio.export(output_path, format="wav")
    return output_path

#-------------------->
'''
FUNCTIONS CONVERT AUDIO
FILES INTO CHUNKS FOR 
FURTHER PROCESS
'''
#-------------------->
def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000

    chunks = []

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start: start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks

#-------------------->
'''
WRITE A FUNCTION TO CHECK
IF THE SOURCE IS IS HTTP
FILE CALL download_youtube_audio
FUNCTION IF NOT THEN CALL
convert_to_wav FUNCTION
'''
#-------------------->
def process_input(source: str) -> list:
    # FIX: Ensure downloads directory always exists before any operation
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    if source.startswith("http://") or source.startswith('https://'):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        # FIX: Check if uploaded local file actually exists
        if not os.path.exists(source):
            raise FileNotFoundError(f"Local file not found: {source}")
        wav_path = convert_to_wav(source)

    print('Chunking audio...')
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks

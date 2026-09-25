import os
import yt_dlp
from pydub import AudioSegment

DOWNLOAD_PATH = "downloads"

os.makedirs(DOWNLOAD_PATH, exist_ok=True)


def download_yt_video(url: str) -> str:
    output_path = os.path.join(
        DOWNLOAD_PATH,
        "%(title)s.%(ext)s"
    )

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "js_runtimes": {
            "deno": {}
        },
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return os.path.splitext(filename)[0] + ".wav"


def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"

    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")

    return output_path


def audio_chunks(audio_path: str, chunk_length_ms: int = 600000) -> list:
    """Split audio into chunks of specified length."""
    audio = AudioSegment.from_file(audio_path)

    chunks = []

    for i, start in enumerate(range(0, len(audio), chunk_length_ms)):
        chunk = audio[start:start + chunk_length_ms]

        chunk_path = f"{audio_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")

        chunks.append(chunk_path)

    return chunks


def process_input(source: str) -> list:
    if source.startswith(("http://", "https://")):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_yt_video(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = audio_chunks(wav_path)

    print(f"Audio ready — {len(chunks)} chunk(s) created.")

    return chunks
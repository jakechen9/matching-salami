import os, pandas as pd
from yt_dlp import YoutubeDL
import shutil

print("yt-dlp:", __import__("yt_dlp").version.__version__)
print("ffmpeg:", shutil.which("ffmpeg"))

df = pd.read_csv("salami_youtube_pairings.csv")
outdir = os.path.join(os.getcwd(), "downloaded_audio")
os.makedirs(outdir, exist_ok=True)

COMMON = {
    "format": "bestaudio/best",
    "ignoreerrors": True,
    "retries": 5,
    "fragment_retries": 5,
    "concurrent_fragment_downloads": 4,
    "quiet": True,
    # Use web client only to avoid Android PO-token warnings
    "extractor_args": {"youtube": {"player_client": ["web"]}},
    # If ffmpeg isn't on PATH, set this:
    # "ffmpeg_location": "/usr/bin",           # Linux example
    # "ffmpeg_location": r"C:\ffmpeg\bin",     # Windows example
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
    # If needed for age/region‑restricted vids:
    # "cookiesfrombrowser": ("chrome",),  # or ("firefox",)
}

for _, row in df.iterrows():
    yt_id = str(row["youtube_id"])
    salami_id = str(row["salami_id"])
    url = f"https://www.youtube.com/watch?v={yt_id}"

    opts = {**COMMON, "outtmpl": os.path.join(outdir, f"{salami_id}.%(ext)s")}
    try:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info:
                print(f"OK {salami_id}")
            else:
                print(f"SKIP {salami_id}: unavailable")
    except Exception as e:
        print(f"FAIL {salami_id}: {e}")

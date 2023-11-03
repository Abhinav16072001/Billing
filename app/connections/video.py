from pytube import YouTube
import requests
import re


def download_youtube_video(url, download_directory):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=download_directory)
        return f"Video from {url} downloaded successfully."
    except Exception as e:
        return f"Error downloading video from {url}: {str(e)}"

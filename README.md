# YouTube Transcript Downloader

Read and download the transcript of a YouTube video using Python

A Python script to fetch and clean up transcripts from YouTube videos using the [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/).

## Features

- Extracts transcript using video ID
- Groups captions into readable paragraphs
- Removes filler tags like `[Music]`
- Saves transcript to a `.txt` file

## Requirements

- Python 3.7+
- See `requirements.txt` for dependencies

Optionally add pytube later if you decide to fetch video titles

Usage
python youtube_transcript.py

Enter a YouTube video ID at the end of the URL when prompted.

The transcript will be saved as:

youtube_transcript_<VIDEO_ID>.txt


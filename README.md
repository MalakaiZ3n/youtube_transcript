# YouTube Transcript Downloader

Read and download the transcript of a YouTube video using Python

A Python script to fetch and clean up transcripts from YouTube videos using the [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/).

## Features

- Extracts transcript using video ID
- Groups captions into readable paragraphs
- Removes filler tags like `[Music]`
- Saves transcript to a `.txt` and `.json` file

## Requirements

- Python 3.7+
- See `requirements.txt` for dependencies

## Usage

```
python youtube_transcript.py
```

Enter a YouTube URL or video ID when prompted.

The transcript will be saved as:

```
transcripts/<SAFE_TITLE>_<VIDEO_ID>.txt
transcripts/<SAFE_TITLE>_<VIDEO_ID>.json
```

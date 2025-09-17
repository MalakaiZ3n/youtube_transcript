import re
import json
from youtube_transcript_api import YouTubeTranscriptApi

def paragraph_cleanup(text, max_len=500):
    sentences = re.split(r'(?<=[.?!])\s+(?=[A-Z])',text.strip())
    paragraphs = []
    current = []

    for sentence in sentences:
        current.append(sentence)
        if sum(len(s) for s in current) > max_len:
            paragraphs.append(" ".join(current))
            current = []

    if current:
        paragraphs.append(" ".join(current))

    return "\n\n".join(paragraphs)

def fetch_transcript(video_id):
    try:
        api = YouTubeTranscriptApi()
        fetched = api.fetch(video_id, languages=['en'])

        # JSON Version
        json_filename = f"youtube_transcript_{video_id}.json"
        with open(json_filename, "w", encoding="utf-8") as jf:
            json.dump([s.__dict__ for s in fetched], jf, indent=2)
        print(f"JSON transcript saved to {json_filename}")

        # Paragraph Cleanup
        lines = " ".join([snippet.text for snippet in fetched])
        cleaned = re.sub(r'\[.*?\]', '', lines).strip()
        formatted = paragraph_cleanup(cleaned)

        # Save using video ID
        filename = f"youtube_transcript_{video_id}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(formatted)

        print(f"Transcript saved to {filename}")

    except Exception as e:
        print(f"\nError getting transcript: {e}")

if __name__ == "__main__":
    video_id = input("Enter the YouTube video ID: ").strip()
    fetch_transcript(video_id)

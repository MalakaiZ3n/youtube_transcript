import re
import json
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp

def extract_video_id(url_or_id):
    """Extract video ID from YouTube URL or return ID if already provided"""
    # If it's already just an 11-character ID, return it
    if re.match(r'^[A-Za-z0-9_-]{11}$', url_or_id):
        return url_or_id
    
    # Pattern to match various YouTube URL formats
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/)([A-Za-z0-9_-]{11})',
        r'youtube\.com\/shorts\/([A-Za-z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    
    # If no pattern matches, assume it's the video ID
    return url_or_id.strip()

def sanitize_filename(title):
    """Remove invalid filename characters"""
    # Replace invalid characters with underscores
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', title)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    # Limit length to avoid filesystem issues
    return sanitized[:200]

def get_video_title(video_id):
    """Fetch video title using yt-dlp"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return info.get('title', video_id)
    except Exception as e:
        print(f"Could not fetch title: {e}")
        return video_id

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

        # Video Title
        video_title = get_video_title(video_id)
        safe_title = sanitize_filename(video_title)

        api = YouTubeTranscriptApi()
        fetched = api.fetch(video_id, languages=['en'])

        # JSON Version
        json_filename = f"{safe_title}_{video_id}.json"
        with open(json_filename, "w", encoding="utf-8") as jf:
            json.dump([s.__dict__ for s in fetched], jf, indent=2)
        print(f"JSON transcript saved to {json_filename}")

        # Paragraph Cleanup
        lines = " ".join([snippet.text for snippet in fetched])
        cleaned = re.sub(r'\[.*?\]', '', lines).strip()
        formatted = paragraph_cleanup(cleaned)

        # Save using video ID
        filename = f"{safe_title}_{video_id}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(formatted)

        print(f"Transcript saved to {filename}")

    except Exception as e:
        print(f"\nError getting transcript: {e}")

if __name__ == "__main__":
    user_input= input("Enter the YouTube video ID: ").strip()
    video_id = extract_video_id(user_input)
    print(f"Processing video ID: {video_id}")
    fetch_transcript(video_id)

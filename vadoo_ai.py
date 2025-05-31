import os
import random
import logging
import requests
import json
import time
from dotenv import load_dotenv

from youtube_upload import upload_video

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="vadoo.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set environment variables and global variables
load_dotenv()
VADOO_KEY = os.getenv('VADOO_KEY')
GENERATE_VIDEO_URL = "https://viralapi.vadoo.tv/api/generate_video"
GET_VIDEO_URL = "https://viralapi.vadoo.tv/api/get_video_url"
HEADER = {"x-api-key": VADOO_KEY}

# Setup lists to choose from for topics, themes, and voices
TOPICS = [
    "Random AI Story",
    "Scary Stories",
    "Motivational",
    "Bedtime Stories",
    "Interesting History",
    "Fun Facts",
    "Long Form Jokes",
    "Life Pro Tips",
    "Philosophy"
]
THEMES = [
    "Hormozi_1",
    "Beast",
    "Tracy",
    "Noah",
    "Karl",
    "Luke",
    "Devin",
    "Hormozi_2",
    "Hormozi_3",
    "Ali",
    "Celine",
    "Maya",
    "Ella",
    "Dan",
    "David",
    "Umi",
    "Iman",
    "William"
]
VOICES = [
    "Charlie",
    "George",
    "Callum",
    "Sarah",
    "Laura",
    "Charlotte"
]
STYLES = [
    "None",
    "3d model",
    "analog film",
    "anime",
    "cartoon",
    "cinematic",
    "comic book",
    "craft clay",
    "digital art",
    "fantasy art",
    "isometric",
    "line art",
    "low poly",
    "neon punk",
    "origami",
    "photographic",
    "pixel art",
    "playground",
    "texture",
    "watercolor"
]
DURATIONS = ["30-60", "60-90", "90-120", "5 min", "10 min"]

# Make a new video and pass parameters then return the ID
def generate_video(payload):
    try:
        logger.info(f"Posting to make new AI Video. . .")
        resp = requests.post(url=GENERATE_VIDEO_URL, headers=HEADER, data=payload)
        generated_vid = json.loads(resp.text)
        video_id = generated_vid["vid"]
        logger.info(f"Generated new AI Video ID: {video_id}")
        return str(video_id)
    except Exception as e:
        logger.error(f"Couldn't generate the video: {e}")
        return False

# Save the AI video locally to post later
def get_video(vid_id):
    # Use the API to generate the download URL
    try:
        logger.info("Retrieving download URL. . .")
        vid_name = 'vid_' + vid_id + '.mp4'
        payload = {"id": vid_id}
        resp = requests.get(url=GET_VIDEO_URL, headers=HEADER, params=payload)
        get_url = json.loads(resp.text)
        download_url = get_url["url"]
        logger.info("Generated download URL")
    except Exception as e:
        logger.error(f"Could not generate download URL: {e}")

    # Download the video with URL generated
    try:
        logger.info("Downloading AI video locally. . .")
        headers = {
            'User-Agent': 'Mozilla/5.0'  # Mimic a browser
        }
        r = requests.get(download_url, headers=headers, stream=True)
        if r.status_code == 200:
            with open("vadoo_vids/" + vid_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        else:
            logger.error(f"Could not download video {vid_id}: {r.text}")
            return False
        
        logger.info("Downloaded Video")
        return vid_name
    except Exception as e:
        logger.error(f"Could not download video {vid_id}: {e}")
        return False

# Start of new video generation, picking a random topic, theme, voice, and style
topic = random.choice(TOPICS)
theme = random.choice(THEMES)
voice = random.choice(VOICES)
style = random.choice(STYLES)
logger.info(f"Starting new video generation, payload-data: topic:{topic} theme:{theme} voice:{voice} style:{style} ")

vid_id = generate_video({
                        "topic": topic,
                        "theme": theme,
                        "voice": voice,
                        "style": style,
                        })
# vid_id = "452921519275"
logger.info("Video is being generated in Vadoo, waiting 5 minutes. . .")
time.sleep(300)
vid_name = get_video(vid_id)

# Push the generated video to YouTube
title = f"{topic} #{vid_id[-4:]}"
description = f"A {topic} told by {voice} in {style}"
if(vid_name):
    upload_video(title=title, description=description, vid_name="vadoo_vids/" + vid_name)
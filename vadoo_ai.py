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
logging.basicConfig(filename="/home/vector/vsCode/espeon/vadoo.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set environment variables and global variables
load_dotenv()
VADOO_KEY = os.getenv('VADOO_KEY')
OPEN_API_KEY = os.getenv('OPEN_API_KEY')
GENERATE_VIDEO_URL = "https://viralapi.vadoo.tv/api/generate_video"
GET_VIDEO_URL = "https://viralapi.vadoo.tv/api/get_video_url"
HEADER = {"x-api-key": VADOO_KEY, "Content-Type": "application/json"}

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
PROMPTS = ["Pandoras Box", "Daedalus and Icarus", "Persephone"]

# Use OpenAI API to generate a story with a title based on a prompt provided
def generate_story(prompt):
    url = "https://open-ai21.p.rapidapi.com/conversationllama"
    payload = {
            "messages":[{
                "role":"user",
                "content":prompt
                }],
            "web_access":False
        }
    headers = {
        "x-rapidapi-key": OPEN_API_KEY,
        "x-rapidapi-host": "open-ai21.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    # Return the story for whatever prompt is given
    try:
        logger.info(f"Finding a story about {prompt}")
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        story = data["result"]
        return story
    except Exception as e:
        logger.error(f"Couldn't generate a custom story: {e}")
        return False

# Make a new video and pass parameters then return the ID
def generate_video(payload):
    try:
        logger.info(f"Posting to make new AI Video. . .")
        resp = requests.post(url=GENERATE_VIDEO_URL, headers=HEADER, json=payload)
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
            with open("/home/vector/vsCode/espeon/vadoo_vids/" + vid_name, 'wb') as f:
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

############################
# Start of new video generation, picking a random topic, theme, voice, and style
############################
topic = random.choice(TOPICS)
theme = random.choice(THEMES)
voice = random.choice(VOICES)
style = random.choice(STYLES)
prompt = random.choices(PROMPTS)
logger.info(f"\nStarting new video generation. . .")

# Generate a story and title based on a random prompt
story_data = generate_story(prompt[0])
if(story_data):
    logger.info(f"Telling story of {prompt[0]}")
    vid_id = generate_video({
        "topic": "Custom",
        "prompt": story_data,
        "voice": voice,
        "style": style,
        "duration": "60-90"
    })

# Create generic shitty AI video
# vid_id = generate_video({
#                         "topic": topic,
#                         "theme": theme,
#                         "voice": voice,
#                         "style": style,
#                         })

# Manual single video run
# vid_id = "582494681685"
# story_data = {
#   "title": "The Ember of Eldrador: A Blaze of Bravery",
#   "story": "As the sun dipped into the horizon, casting a fiery glow over the land, Eira Shadowglow stood at the edge of the mystical forest, her eyes fixed on the ancient dragon, Tharros the Unyielding. The beast's scales glistened like polished obsidian, and its fiery breath illuminated the darkening sky. Eira's mission was clear: rescue Princess Lyra, the last heir of the Eldridian throne, from Tharros' clutches. The dragon had taken the princess to its lair, deep within the heart of the forest, and Eira was determined to put an end to its reign of terror. With her trusty sword, Ember, at her side, Eira charged forward, her heart pounding in her chest. The air was thick with the scent of smoke and ash as she battled her way through the treacherous terrain, dodging Tharros' flames and striking back with precision. As she approached the lair, the dragon's roar grew louder, and Eira could feel the ground shaking beneath her feet. With a fierce cry, she burst into the lair, her sword flashing in the dim light. Tharros loomed before her, its eyes blazing with fury. The battle was fierce, the two combatants exchanging blows and neither gaining the upper hand. But Eira refused to yield, her determination fueled by the thought of Lyra's innocent face. In a final, desperate bid to defeat the dragon, Eira unleashed a mighty swing of Ember, striking true and shattering Tharros' scales. The beast let out a deafening roar as it stumbled, its flames dying out. Eira seized the opportunity, striking the final blow and sending Tharros crashing to the ground. With the dragon defeated, Eira rushed to Lyra's side, freeing her from her prison. Together, they escaped the lair, and as they emerged into the bright sunlight, Eira knew that her bravery had saved not only the princess, but also the kingdom itself."
# }

# Make sure a video was generated before downloading/posting
if(vid_id):
    logger.info("Video is being generated in Vadoo, waiting 10 minutes. . .")
    time.sleep(600)
    vid_name = get_video(vid_id)

    # Make sure the video was downloaded, then push the video to YouTube
    title = f"{topic} #{vid_id[-4:]}"
    description = f"A {topic} told by {voice} in {style}"
    if(vid_name):
        upload_video(title=prompt[0], description=story_data, vid_name="vadoo_vids/" + vid_name)
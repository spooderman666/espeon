import os
import logging
from dotenv import load_dotenv
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
from moviepy.editor import VideoFileClip, concatenate_videoclips

load_dotenv()
LOG_PATH = '/home/vector/vsCode/espeon/vadoo.log'
logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
absolute_path = '/home/vector/vsCode/espeon/'

##################################################################
# Add trimmed Jigglypuff song to the end of videos
##################################################################
def merge_videos(vid_name):
    print('Adding Jigglypuff Song. . .')
    logger.info('Adding Jigglypuff Song. . .')
    video_file_list = [absolute_path + vid_name, absolute_path + 'jiggle_song.mp4']
    loaded_video_list = []
    for video in video_file_list:
        print(f"Adding video file:{video}")
        loaded_video_list.append(VideoFileClip(video))
    final_clip = concatenate_videoclips(loaded_video_list, method='compose')
    merged_video_name = vid_name + '_merged'
    final_clip.write_videofile(absolute_path + f"{merged_video_name}.mp4")

##################################################################
# Upload to youtube
##################################################################
def upload_video(title, description, vid_name): 
    # merge_videos(vid_name=vid_name)
    logger.info('Uploading. . .')
    # loggin into the channel
    channel = Channel()
    channel.login(absolute_path + "client_secret.json", absolute_path + "storage_path")

    # setting up the video that is going to be uploaded
    video = LocalVideo(file_path = absolute_path + vid_name)

    # setting snippet
    if(len(title) > 100):
        title = title[0:90] + '...'
    video.set_title(title)
    video.set_description(description)
    # video.set_tags(tags)
    # video.set_category(category)
    video.set_default_language("en-US")

    try:
        video = channel.upload_video(video)
    except:
        # print('playlist error')
        print(video)
        logger.info('error?')


    # Remove all videos except jiggly
    # logger.info('Cleaning. . .')
    # files = os.listdir()
    # for file in files:
    #     if(file.endswith('.mp4') and file != 'jiggle_song.mp4'):
    #         os.remove(file)

# upload_video("test_vid", "testing upload", "to_upload.mp4")
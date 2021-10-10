import json
import time
from requests import get, post
from video_indexer import VideoIndexer

CONFIG = {
    'SUBSCRIPTION_KEY': '4175d484f56248b6bf0be8d0cc484488',
    'LOCATION': 'trial',
    'ACCOUNT_ID': '1d891655-96dd-4acd-a971-4a1fe17ce312'
}

vi = VideoIndexer(
    vi_subscription_key=CONFIG['SUBSCRIPTION_KEY'],
    vi_location=CONFIG['LOCATION'],
    vi_account_id=CONFIG['ACCOUNT_ID']
)

video = vi.upload_to_video_indexer(
   input_filename='VID_20211004_184045.mp4',
   video_name='passanger4',
   video_language='English'
)
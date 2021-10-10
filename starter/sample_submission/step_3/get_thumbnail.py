import json
import time
import sys, os
from video_indexer import VideoIndexer
import time
from requests import get, post

# VIDEO INDEXER API DOCUMENTATION: https://api-portal.videoindexer.ai/api-details#api=Operations&operation=Get-Video-Index

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

files_dict = {}

# https://api-portal.videoindexer.ai/api-details#api=Operations&operation=Create-Person-Model
def create_person_model(location, accountId, name, accessToken: None):
    params = {"accessToken": accessToken}
    resp = post("https://api.videoindexer.ai/{}/Accounts/{}/Customization/PersonModels?name={}".format(location, accountId, name), params=params).json()

    return resp['id']

# https://api-portal.videoindexer.ai/api-details#api=Operations&operation=Create-Person
def create_person(location, accountId, personModelId, name, accessToken: None):
    params = {"accessToken": accessToken}
    resp = post("https://api.videoindexer.ai/{}/Accounts/{}/Customization/PersonModels/{}/Persons?name={}".format(location, accountId, personModelId, name), params=params).json()

    return resp['id']

# https://api-portal.videoindexer.ai/api-details#api=Operations&operation=Create-Custom-Face
def create_custom_face(location, accountId, personModelId, personId, accessToken: None):
    params = {"accessToken": accessToken}
    resp = post("https://api.videoindexer.ai/{}/Accounts/{}/Customization/PersonModels/{}/Persons/{}/Faces".format(location, accountId, personModelId, personId), files=files_dict, params=params).json()

    return resp[3]

def get_custom_face_picture(name, surname):

    #Remove the print to the standard output to keep the display clean
    blockPrint()

    video_info = vi.get_video_info("02e4b689eb")
    thumbnail_id = video_info['summarizedInsights']['faces'][0]['thumbnailId']
    video_thumbnail = vi.get_thumbnail_from_video_indexer("02e4b689eb", thumbnail_id)
    thumbnails = video_info['videos'][0]['insights']['faces'][0]['thumbnails']

    for thumbnail in thumbnails:
        thumbnail_id = thumbnail['id']
        file_name = thumbnail['fileName']
        video_thumbnail = vi.get_thumbnail_from_video_indexer("02e4b689eb", thumbnail_id)
        files_dict[file_name] = video_thumbnail

    accessToken = vi.get_access_token()

    enablePrint()

    person_model = create_person_model(vi.vi_location, vi.vi_account_id, (name+surname+'_PersonModel'), accessToken)
    person = create_person(vi.vi_location, vi.vi_account_id, person_model, (name+surname+'_Person'), accessToken)
    custom_face = create_custom_face(vi.vi_location, vi.vi_account_id, person_model, person, accessToken)

    params = {"accessToken": accessToken}
    resp = get("https://api.videoindexer.ai/{}/Accounts/{}/Customization/PersonModels/{}/Persons/{}/Faces/{}".format(vi.vi_location, vi.vi_account_id, person_model, person, custom_face), params=params)

    return resp.content


def get_sentiments():
    sentiments = video_info['summarizedInsights']['sentiments']
    print('Sentiments: ', sentiments)

def get_emotions():
    emotions = video_info['summarizedInsights']['emotions']
    print('Emotions: ', emotions)

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__
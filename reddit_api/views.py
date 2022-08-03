from concurrent.futures import thread
from fileinput import filename
import math
import os
import threading

from django.http import HttpResponse, HttpResponseNotFound

from django.http import JsonResponse
from core_system.reddit.index import getRedditClientInstance
from core_system.video_creation.voices import save_text_to_mp3
from core_system.storage_bucket.index import getS3StorageInstance
from core_system.video_creation.screenshot_downloader import download_screenshots_of_reddit_posts
from core_system.video_creation.background import get_background_config,download_background,chop_background_video
from core_system.video_creation.final_video import make_final_video
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def get_list_of_sub_reddits(req):
    return JsonResponse({
        'subreddits':[
            "subredditoftheday",
            "askhistorians",
            "suggestmeabook",
            "podcasts",
            "skincareaddiction",
            "bodyweightfitness",
            "netflixbestof",
            "games"
        ]
    })


def get_post_from_id(req):
    post_id = req.GET["post_id"]
    reddit_client= getRedditClientInstance()
    post=reddit_client.get_post_by_id(post_id=post_id)
    return JsonResponse(post)

@csrf_exempt
def get_comments_from_post_id(req):
    username=req.POST["username"]
    post_id = req.POST["post_id"]
    if not username or not post_id:
        return JsonResponse({
            "message":"Please username or post_id invalid",
            "status":"500"
        })
    reddit_client= getRedditClientInstance()
    comments=reddit_client.get_top_comments_by_post(post_id=post_id,max_comment_length=500)
    length, number_of_comments = save_text_to_mp3(comments,username=username)
    length=math.ceil(length)

    download_screenshots_of_reddit_posts(comments, number_of_comments,theme="light",username=username,lang="en")
    bg_config = get_background_config(background_choice="motor-gta")
    download_background(bg_config)
    chop_background_video(bg_config, length,username)
    save_path=make_final_video(number_of_comments, length, comments, bg_config,username)

    #was for s3 but don't want to use it right now
    # asset_path=os.path.join(os.getcwd(),"assets",username)

    # s3StorageClient=getS3StorageInstance()
    # task=threading.Thread(target=s3StorageClient.upload_file,args=(f"{asset_path}/temp/mp3/*.mp3","tiktok-video-maker",f"{username}/temp/mp3",))
    # task.start()    
    print(save_path)
    return send_file_response(req,save_path)


def send_file_response(request, file_location):
    filename=file_location.split("/")[-1]
    try:    
        with open(file_location, 'rb') as f:
           file_data = f.read()

        # sending response 
        response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

    except IOError:
        # handle file not exist case here
        response = HttpResponseNotFound('<h1>File not exist</h1>')
    return response
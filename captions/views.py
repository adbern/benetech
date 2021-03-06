from django.shortcuts import render
from django.http import HttpResponse
import sys
import os
import requests
import json
import simplejson

def index(request):
    return HttpResponse("Hello world")
    
def amara(request, youtube_id):

   #http://amara.org/api2/partners/videos/?video_url=http://www.youTube.com/watch?v=8OnfLEDAcB4&format=json
   url_amara = "http://amara.org/api2/partners/videos/?video_url=http://www.youTube.com/watch?v=" + youtube_id + "&format=json" 
   result_amara = requests.get(url_amara)  
   amara_data = json.loads(result_amara.content)
   amara_totalcount = amara_data["meta"]["total_count"] # >1 or null  

   # parse json and test totalcount and languages fields from Amara
   if amara_totalcount >= 1:
       amara_languages = amara_data["objects"][0]["languages"]
       if len(amara_languages) != 0:
           amara_response = True
       else: 
           amara_response = False
   else:
       amara_response = False
       
       
   response_data = {
       "status" : "success",
       "data" : { "captions" : amara_response,        
       }
   }

   return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')
    
def youTube(request, youtube_id):
    
    #youtube check
    url_youTube = "https://www.googleapis.com/youtube/v3/videos?id=" + youtube_id + "&part=contentDetails&key=AIzaSyD7c2JM-xjKq1PGfSGmg6JYrjwSlpHcW0c"  
    result_youTube = requests.get(url_youTube)
    youTube_data = json.loads(result_youTube.content)
    
    #checking JSON for video ID error response
    if not youTube_data["items"]:
        error_response = True
    else: 
        error_response = False
        youTube_response = youTube_data["items"][0]["contentDetails"]["caption"];  
    
        if youTube_response == "true":
            youTube_response = True
        else:
            youTube_response = False
    
    #API requests have failed for YouTube
    if error_response:
         response_data = {
             "status" : "error",
             "data" : None,
             "message": "YouTube request failed, check YouTube ID."
         }
    else: #API  request has succeeded 
    
        response_data = {
            "status" : "success",
            "data" : { "captions" : youTube_response,     
            }
        }

    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')


    
def youTubeAmara(request, youtube_id):
    
    #youtube check
    url_youTube = "https://www.googleapis.com/youtube/v3/videos?id=" + youtube_id + "&part=contentDetails&key=AIzaSyD7c2JM-xjKq1PGfSGmg6JYrjwSlpHcW0c"  
    result_youTube = requests.get(url_youTube)
    youTube_data = json.loads(result_youTube.content)
    
    #checking JSON for video ID error response
    if not youTube_data["items"]:
        error_response = True
    else: 
        error_response = False
        youTube_response = youTube_data["items"][0]["contentDetails"]["caption"];  
    
        if youTube_response == "true":
            youTube_response = True
        else:
            youTube_response = False
    
    #amara check
    #http://amara.org/api2/partners/videos/?video_url=http://www.youTube.com/watch?v=8OnfLEDAcB4&format=json
    url_amara = "http://amara.org/api2/partners/videos/?video_url=http://www.youTube.com/watch?v=" + youtube_id + "&format=json" 
    result_amara = requests.get(url_amara)  
    amara_data = json.loads(result_amara.content)
    amara_totalcount = amara_data["meta"]["total_count"] # >1 or null  
    
    # parse json and test totalcount and languages fields from Amara
    if amara_totalcount >= 1:
        amara_languages = amara_data["objects"][0]["languages"]
        if len(amara_languages) != 0:
            amara_response = True
        else: 
            amara_response = False
    else:
        amara_response = False
        
    #API requests have failed for Amara and YouTube
    if error_response and not amara_response:
         response_data = {
             "status" : "error",
             "data" : None,
             "message": "YouTube and Amara API request fail, check video ID"
         }
    else: #API  requests have succeeded 
        response = youTube_response or amara_response        
        
        response_data = {
            "status" : "success",
            "data" : { "amara_captions" : amara_response, "youtube_captions" : youTube_response, "captions" : response         
            }
        }

    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')
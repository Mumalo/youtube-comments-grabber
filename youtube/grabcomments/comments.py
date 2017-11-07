import  httplib2
import os
import sys
import csv
from urllib.parse import urlparse, parse_qs

from googleapiclient.discovery import build_from_document, build
from googleapiclient.errors import HttpError

CLIENT_SECRETS_FILE = "client_secrets.json"
DEVELOPER_KEY = "AIzaSyCXnEFcvqXBSneWmx0ldq3HlIJcJCvjqbA"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

myFileds = ["UserName", "Date", "Star Rating", "Review or Comment", "link"]
comments = {"comment":[]}
parent_ids = []
video_url = "https://www.youtube.com/watch?v=esQBYPTMm1k"

def get_id(video_url):
    u_pars = urlparse(video_url)
    quer_v = parse_qs(u_pars.query).get('v')
    if quer_v:
        return quer_v[0]
    pth = u_pars.path.split('/')
    if pth:
        return pth[-1]

def grab_comments(dict):
    myFile = open("comments.csv", "w", encoding='utf-8', newline='')
    with myFile:
        myFileds = ["UserName", "Date", "Star Rating", "Review or Comment", "link"]
        writer = csv.DictWriter(myFile, fieldnames=myFileds, dialect='excel-tab')
        writer.writeheader()
        for c in dict["comment"]:
            writer.writerow(c)

def get_comments_for_comment(parent_id, max=100, token=None):
    next_page_token = ''
    while (next_page_token is not None):
        results = youtube.comments().list(
            part="snippet",
            parentId=parent_id,
            textFormat="plainText",
            maxResults=max,
            pageToken=next_page_token,
        ).execute()

        next_page_token = results.get("nextPageToken", None)
        for item in results["items"]:
            comment = item["snippet"]
            id = item["id"]
            author = comment["authorDisplayName"]
            rating = comment["likeCount"]
            date = comment["publishedAt"]
            text = comment["textOriginal"]
            url = video_url + "&lc=" + id
            comments["comment"].append({"UserName":author, "Date":date, "Star Rating":rating, "Review or Comment":text, "link":url})


def get_comments_for_video(video_id, token=None, max=100):
    next_page_token = ''
    while next_page_token is not None:
        results = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,
            textFormat="plainText",
            order="relevance",
            maxResults=max,
            pageToken=next_page_token
        ).execute()


        for item in results["items"]:
            id = item["id"]
            comment = item["snippet"]["topLevelComment"]["snippet"]
            author = comment["authorDisplayName"]
            rating = comment["likeCount"]
            date = comment["publishedAt"]
            text = comment["textOriginal"]
            url = video_url + "&lc=" + id
            comments["comment"].append({"UserName":author, "Date":date, "Star Rating":rating, "Review or Comment":text, "link":url})
            replyCount = item["snippet"]["totalReplyCount"]
            if ( replyCount > 0):
                id = item["id"]
                parent_ids.append(id)

            next_page_token = results.get("nextPageToken", None)

video_id = get_id(video_url=video_url)
get_comments_for_video(video_id=video_id)
for id in parent_ids:
    get_comments_for_comment(parent_id=id)

print(len(comments["comment"]))
grab_comments(dict=comments)

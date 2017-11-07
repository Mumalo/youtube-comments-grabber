from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import UrlForm
from django.shortcuts import HttpResponse
from urllib.parse import urlparse, parse_qs
import httplib2
import os
import sys
import csv

#import youtube api libraries here
from .secret import CLIENT_SECRETS_FILE, DEVELOPER_KEY, YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, youtube


comments = {"comment":[]}
parent_ids = []
video_url = []

def get_id(video_url):
    u_pars = urlparse(video_url)
    quer_v = parse_qs(u_pars.query).get('v')
    if quer_v:
        return quer_v[0]
    pth = u_pars.path.split('/')
    if pth:
        return pth[-1]

def get_url(request):
    form = UrlForm(data=request.GET)
    if form.is_valid():
        url = form.cleaned_data.get('url', None)
        id = get_id(video_url=url)
        get_comments_for_video(request, video_id=id)
        if len(parent_ids) > 0:
            for id in parent_ids:
                get_comments_for_comment(request, parent_id=id)
        # return HttpResponseRedirect(reverse('grab', args=[]))
        data = [['First row', 'Foo', 'Bar', 'Baz'],['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"]]
        return grab_comments(request, data=comments)
    return render(request, 'grabcomments/grab.html', {'form':form})

def grab_comments(request, data):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="comments.csv"'

    myFileds = ["UserName", "Date", "Star Rating", "Review or Comment", "link"]
    writer = csv.DictWriter(response, fieldnames=myFileds, dialect='excel-tab')
    writer.writeheader()
    for d in data["comment"]:
        writer.writerow(d)


    return response


def get_comments_for_comment(request, parent_id, max=100, token=None):
    next_page_token = ''
    video_url = ''
    if 'url' in request.GET:
        video_url = request.GET.get('url')
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

def get_comments_for_video(request, video_id, token=None, max=100):
    video_url = ''
    if 'url' in request.GET:
        video_url = request.GET.get('url')
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

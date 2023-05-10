from dotenv import load_dotenv
from googleapiclient.discovery import build
from SearchEngine import entity_recognition as er
import os
import re

class youtubeAPI():
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.API_KEY)
    
    def ensure_shorts(self, video_id):
        response = self.youtube.videos().list(
            part='contentDetails',
            id=",".join(video_id)
        ).execute()
        data=[[i['contentDetails']['duration'],i['id']] for i in response['items']]
        pattern1 = r'^PT[0123]M\d{1,2}S$'
        pattern2 = r'^PT\d{1,2}S$'
        result =[i[1] for i in data if(re.match(pattern1, i[0]) or re.match(pattern2, i[0]))]
        return result

    def trending_search(self, country, pagetoken=None):
        if pagetoken == None:
            response = self.youtube.videos().list(
                part='snippet',
                chart='mostPopular',
                regionCode=country,
                maxResults=50
            ).execute()
        else:
            response = self.youtube.videos().list(
                part='snippet',
                chart='mostPopular',
                regionCode=country,
                maxResults=50,
                pageToken=pagetoken
            ).execute()
        pagetoken = response['nextPageToken']
        ids =[item['id'] for item in response['items']]
        return (ids, pagetoken)

    def query_youtube(self, query, country, pagetoken = None, max_results=50):
        if pagetoken == None:
            search_response = self.youtube.search().list(
                part='id',
                type='video',
                q=query,
                regionCode=country,
                videoEmbeddable='true',
                maxResults=max_results
            ).execute()
        else:
            search_response = self.youtube.search().list(
                part='id',
                type='video',
                q=query,
                regionCode=country,
                videoEmbeddable='true',
                maxResults=max_results,
                pageToken=pagetoken
            ).execute()

        # Extract the video IDs from the search response
        pagetoken = search_response['nextPageToken']
        video_ids = [item['id']['videoId'] for item in search_response['items']]
        return (video_ids, pagetoken)

        # Make a request to retrieve video statistics for each ID
    def get_statistics(self, video_ids):
        videos_response = self.youtube.videos().list(
             part='statistics',
             id=','.join(video_ids)
         ).execute()
         # Create a list of lists containing video IDs, views, and likes
        result = []
        for item in videos_response['items']:
            video_id = item['id']
            views = int(item['statistics'].get('viewCount', 0))
            likes = int(item['statistics'].get('likeCount', 0))
            result.append([video_id, views, likes])
        return result


def search_for_entity(prompt, country, pagetoken = None):
    entity = er.recognize(prompt)
    #print(entity)
    obj = youtubeAPI()
    if(len(entity) == 0):
        query = prompt
        data = obj.query_youtube(query, country, pagetoken, 50)
    else:
        query1 = "AND".join(entity)
        data = obj.query_youtube(query1, country, pagetoken, 50)

    #result = sorted(result, key=lambda x: (x[1]+x[2]), reverse=True) #possible sorting method
    ids = data[0]
    result = obj.ensure_shorts(ids)
    return(result, data[1])


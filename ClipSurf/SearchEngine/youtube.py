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

    def trending_search(self):
        response = self.youtube.videos().list(
            part='snippet',
            chart='mostPopular',
            regionCode='US',
            maxResults=50
        ).execute()
        ids =[item['id'] for item in response['items']]
        return ids

    def query_youtube(self, query, max_results=20):
        search_response = self.youtube.search().list(
            part='id',
            type='video',
            q=query,
            maxResults=max_results
        ).execute()

        # Extract the video IDs from the search response
        video_ids = [item['id']['videoId'] for item in search_response['items']]

        # Make a request to retrieve video statistics for each ID
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

    def get_length(self, video_id):
        response = self.youtube.videos().list(
            part='contentDetails',
            id=video_id
        ).execute()
        data=[[i['contentDetails']['duration'],i['id']] for i in response['items']]
        return data

def search_for_entity(prompt):
    entity = er.recognize(prompt)
    #print(entity)
    result = []
    obj = youtubeAPI()
    if(len(entity) == 0):
        query = prompt
        result.extend(obj.query_youtube(query, 50))
    else:
        query1 = "AND".join(entity)
        query2 = "OR".join(entity)
        result.extend(obj.query_youtube(query1, 25))
        result.extend(obj.query_youtube(query2, 25))

    #result = sorted(result, key=lambda x: (x[1]+x[2]), reverse=True) #possible sorting method
    result = [item[0] for item in result]
    result = obj.get_length(",".join(result))
    pattern1 = r'^PT[012]M\d{1,2}S$'
    pattern2 = r'^PT\d{1,2}S$'
    result =[i for i in result if(re.match(pattern1, i[0]) or re.match(pattern2, i[0]))]
    return result


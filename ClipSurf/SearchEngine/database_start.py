from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
load_dotenv()

username = os.getenv('USER')
password = os.getenv('DATAPASSKEY')

uri = f"mongodb+srv://{username}:{password}@clipsurf.upczxaf.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

class database():
    
    def __init__(self):
        try:
            client.admin.command('ping')
        except Exception as e:
            print(e)
            return "Error"

        db = client["User_Video_Data"]
        self.collection = db['saved_videos']
    
    def insert(self, email_id, video_id):
        result = self.collection.find_one({'email_id' : email_id})
        if result == None:
            document = {
                'email_id' : email_id,
                'video_id' : video_id
            }
            self.collection.insert_one(document)
        else:
            result["video_id"] = result["video_id"] + ',' + video_id
        return
    
    def find(self, email_id):
        result = self.collection.find_one({'email_id' : email_id})
        if result == None:
            return None
        else:
            return result["video_id"].split(",")
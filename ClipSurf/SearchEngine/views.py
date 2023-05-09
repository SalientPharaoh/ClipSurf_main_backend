from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from SearchEngine import database_start as db
from SearchEngine import youtube as yt
from SearchEngine import youtube_bypass as ytb
import json

# Create your views here.
@csrf_exempt 
def trending(request):
    #returns the top trending videos of the youtube global
    obj = yt.youtubeAPI()
    data =obj.trending_search()
    return JsonResponse({'code' : 200, 'data' : data})

@csrf_exempt    
def search(request):
    #searches the youtube based on the entities recognized
    if request.method == 'POST':
        recieved_data = json.loads(request.body.decode('utf-8'))
        try:
            data = yt.search_for_entity(recieved_data['query'])
            return JsonResponse({'code' : 200, 'data' : data})
        except:
            return JsonResponse({'code' : 404})

@csrf_exempt       
def saved(request, email_id):
    #returns the list of the saved videos of the user
    try:
        obj = db.database()
        result = obj.find(email_id)
        if result == None:
            return JsonResponse({'code': 404})
        else:
            return JsonResponse({'code' : 200 ,'data': result})
    except:
        return JsonResponse({'code' : 414})

@csrf_exempt 
def liked(request, email_id, video_id):
    #adds the video id to the list of the user identified by email_id

    obj=db.database()
    try:
        obj.insert(email_id, video_id)
        return JsonResponse({'code': 200, 'status': 'Successful'})
    except:
        return JsonResponse({'code': 404, 'status': 'Failed'})


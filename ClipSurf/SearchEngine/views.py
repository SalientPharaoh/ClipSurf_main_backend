from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from SearchEngine import database_start as db
from SearchEngine import youtube as yt

import json

# Create your views here.
@csrf_exempt 
def trending(request, country):
    obj = yt.youtubeAPI()
    #loading next page data
    if request.method == 'POST':
        recieved_data = json.loads(request.body.decode('utf-8'))
        pagetoken = recieved_data['pagetoken']
        result = obj.trending_search(country, pagetoken)
        data = result[0]
        pagetoken = result[1]
        data = obj.ensure_shorts(data)
        return JsonResponse({'code' : 200, 'data' : data, 'pagetoken' : pagetoken})

    #returns the top trending videos of the youtube global
    result = obj.trending_search(country)
    data = result[0]
    pagetoken = result[1]
    data = obj.ensure_shorts(data)
    return JsonResponse({'code' : 200, 'data' : data, 'pagetoken' : pagetoken})

@csrf_exempt    
def search(request):
    #searches the youtube based on the entities recognized
    if request.method == 'POST':
        recieved_data = json.loads(request.body.decode('utf-8'))
        try:
            if 'pagetoken' in recieved_data:
                data = yt.search_for_entity(recieved_data['query'], recieved_data['country'], recieved_data['pagetoken'])
            else:
                data = yt.search_for_entity(recieved_data['query'], recieved_data['country'])
            pagetoken = data[1]
            result = data[0]
            return JsonResponse({'code' : 200, 'data' : result, 'pagetoken' : pagetoken})
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
        return JsonResponse({'code' : 500})

@csrf_exempt 
def liked(request, email_id, video_id):
    #adds the video id to the list of the user identified by email_id

    obj=db.database()
    try:
        obj.insert(email_id, video_id)
        return JsonResponse({'code': 200, 'status': 'Successful'})
    except:
        return JsonResponse({'code': 404, 'status': 'Failed'})


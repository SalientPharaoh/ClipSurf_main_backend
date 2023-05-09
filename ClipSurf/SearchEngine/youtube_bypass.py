def search():
    import requests
    url = 'https://yt.lemnoslife.com/noKey/videos?part=snippet&chart=mostPopular&shorts=True&regionCode=US&maxResults=9'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        data=[item['id'] for item in enumerate(data['items'])]
        print(data)
    else:
        print('Error:', response.status_code)


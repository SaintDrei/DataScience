##https://stackoverflow.com/questions/48253741/youtube-api-v3-and-python-to-generate-list-of-views-likes-on-own-youtube-videos

YOUTUBE_API_SERVICE_NAME = "YT Scrape"

DEVELOPER_KEY = "AIzaSyD219nFrCNi8ngT7kd_xnfpHVPXDRBBp84"


def youtube_search_list(q, max_results=10):
  # Call the search.list method to retrieve results matching the specified
  # query term.
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
    search_response = youtube.search().list(
        q=q,
        part='id,snippet',
        maxResults=max_results,
        order='viewCount'
      ).execute()

    return search_response

def youtube_search_video(q='spinners', max_results=10):
    max_results = max_results
    order = "viewCount"
    token = None
    location = None
    location_radius = None
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,         
    developerKey=DEVELOPER_KEY)
    q=q
    #Return list of matching records up to max_search
    search_result = youtube_search_list(q, max_results)

    videos_list = []
    for search_result in search_result.get("items", []):

        if search_result["id"]["kind"] == 'youtube#video':
            temp_dict_ = {}
            #Available from initial search
            temp_dict_['title'] = search_result['snippet']['title']  
            temp_dict_['vidId'] = search_result['id']['videoId']  

            #Secondary call to find statistics results for individual video
            response = youtube.videos().list(
                part='statistics, snippet', 
                id=search_result['id']['videoId']
                    ).execute()  
            response_statistics = response['items'][0]['statistics']
            response_snippet = response['items'][0]['snippet']


            snippet_list = ['publishedAt','channelId', 'description', 
                            'channelTitle', 'tags', 'categoryId', 
                            'liveBroadcastContent', 'defaultLanguage', ]
            for val in snippet_list:
                try:
                    temp_dict_[val] = response_snippet[val]
                except:
                    #Not stored if not present
                    temp_dict_[val] = 'xxNoneFoundxx'    

            stats_list = ['favoriteCount', 'viewCount', 'likeCount', 
                          'dislikeCount', 'commentCount']
            for val in stats_list:
                try:
                    temp_dict_[val] = response_statistics[val]
                except:
                    #Not stored if not present
                    temp_dict_[val] = 'xxNoneFoundxx'

            #add back to main list
            videos_list.append(temp_dict_)

    return videos_list
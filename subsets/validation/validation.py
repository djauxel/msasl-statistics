import os
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs
from dotenv import load_dotenv
import googleapiclient.discovery

def parse_video_url(url):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

load_dotenv()

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
DEVELOPER_KEY = os.getenv('YOUTUBE_DATA_API_KEY')

youtube = googleapiclient.discovery.build(
    API_SERVICE_NAME, API_VERSION, developerKey = DEVELOPER_KEY
)

val_file = open('C:\\Projects\\msasl-statistics\\subsets\\validation\\MSASL_val.json')
json_data = json.load(val_file)
val_file.close()

video_list = []

for item in json_data:
    video = { 'url': None, 
                'start_time': None, 
                'end_time': None, 
                'label': None,
                'signer_id': None, 
                'box': None, 
                'text': None, 
                'width': None,
                'height': None, 
                'fps': None }

    video['url'] = item['url'] if 'https://' in item['url'] else 'https://' + item['url']
    video['start_time'] = item['start_time']
    video['end_time'] = item['end_time']
    video['label'] = item['label']
    video['signer_id'] = item['signer_id']
    video['box'] = item['box']
    video['text'] = item['text']
    video['width'] = item['width']
    video['height'] = item['height']
    video['fps'] = item['fps']

    video_id = parse_video_url(video['url'])

    request = youtube.videos().list(
        part = 'status',
        id = video_id
    )

    response = request.execute()

    if response['items']:
        if response['items'][0]['status']['privacyStatus'] == 'public':
            video_list.append(video)

with open('C:\\Projects\\msasl-statistics\\subsets\\validation\\MSASL_val_public.json', 'w') as fp:
    fp.write(
        '[' +
        ',\n'.join(json.dumps(i) for i in video_list) +
        ']')
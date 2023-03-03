import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import datetime

url = 'http://65.2.177.76/api/add-video'
now = datetime.datetime.now(datetime.timezone.utc)
date_time_str = now.isoformat()
data = {
    'device_id' : str(797833),
    'video_file': ('vv.mp4', open('./a5HofBMQ76eetCor3LCydTiDrzFbvXzHksEI9G4t.mp4', 'rb'), 'text/plain')
}

multipart_data = MultipartEncoder(data)

server = requests.post(url, data=multipart_data, headers={'Content-Type': multipart_data.content_type})
output = server.text

print('The response from the server is: \n', output)

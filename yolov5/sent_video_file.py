import requests
def sent_video(device_id):
    url = "http://as99.zvastica.solutions/appapi/submitviolence"
    #payload = {'device_id': '1234'
    device_id = device_id.replace("\"", "")
    payload = {'device_id': device_id}
    #payload = "{\'device_id\': " + device_id + "00" + "}"
    print(payload)
    files = [
    ('file', open('./output.mp4','rb'))
    ]
    headers = {
    'Cookie': 'ci_session=sn7n11lsss9vdlrej79sq6s1o0c5mm3r'
    }

    response = requests.request("POST", url, headers=headers, data = payload, files = files)

    print(response.text.encode('utf8'))

    return True

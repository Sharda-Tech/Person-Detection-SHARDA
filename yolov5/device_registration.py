

def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"
 
  return cpuserial


import requests

def register(myserial):
	url = "http://as99.zvastica.solutions/appapi/adddevicebyhardware"

	#payload="{\n   \n \"hardwar_id\" : % \n      \n        \n}"% (myserial)
	payload = "{ \n \n \"hardwar_id\" : \"" + myserial + "\" \n \n \n}"
	print(payload)
	headers = {
  		'Content-Type': 'application/json',
  		'Cookie': 'ci_session=jsunnmfv9mlfgs7cbcu0nlt8rg2op8up'
		}

	response = requests.request("POST", url, headers=headers, data=payload)

	print(response.text)
	



myserial = getserial()
print(myserial)
register(myserial)

import requests, re, json, uuid

def updateip():
  with open('config.json', 'r') as config_file:
    data=config_file.read()
    token = json.loads(data)

  mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
  ext_ip = requests.get('https://api.ipify.org').text
  print(ext_ip)
  response = requests.post('https://www.always-onward.com/api/device/updateip',
    data = json.dumps({'mac': mac, 'ip': ext_ip}),
    headers={'Authorization': 'Bearer '+token['token']},
    stream=True)
  print(response.text)
  return response.text

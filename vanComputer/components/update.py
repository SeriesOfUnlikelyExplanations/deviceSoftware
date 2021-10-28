import requests, tarfile, os, subprocess, json

def update():
  with open('config.json', 'r') as config_file:
    data=config_file.read()
    config = json.loads(data)
    
  response = requests.get('https://www.always-onward.com/api/device/update',
    params={'version': config['version']},
    headers={'Authorization': 'Bearer '+config['token']},
    stream=True)

  print('Status code: '+str(response.status_code))
  if response.status_code == 200:
    response.raise_for_status()
    print('Updating software')
    with open('vanComputer.tar.gz', 'wb') as f:
      for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
    # open file
    f = tarfile.open('vanComputer.tar.gz')
    f.extractall('.')
    f.close()
    os.remove('vanComputer.tar.gz')
    #call setup shell script here
    subprocess.run(['pipenv', 'install', '--system'])
    print('Update Complete')
    return 'Update Complete'
  else:
    print('Software update not needed')
    return 'Software update not needed'

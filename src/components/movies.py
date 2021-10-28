import requests, os, json

def movies():
  with open('config.json', 'r') as config_file:
    data=config_file.read()
    config = json.loads(data)

  file_list=os.listdir(config['moviesDir'])

  response = requests.get('https://www.always-onward.com/api/device/getmovie',
    params={'movies':','.join(file_list)},
    headers={'Authorization': 'Bearer '+config['token']},
    stream=True)

  if response.status_code == 204:
    print('Movies are up to Date')
    return 'Movies are up to Date'
  elif response.status_code == 200:
    action = response.json()
    if action['status'] == 'movieToDownload':
      print('downloading movie')
      movie = requests.get(action['url'], stream=True)
      movie.raise_for_status()
      print('downloading '+action['name'])
      with open(config['moviesDir'] + '/' + action['name'], 'wb') as f:
        for chunk in movie.iter_content(chunk_size=8192):
          f.write(chunk)
      return action['name'] + ' downloaded'
    elif action['status'] == 'movieToDelete':
      os.remove(config['moviesDir'] + '/' + action['name'])
      return action['name'] + ' deleted'
  else:
    print('error - ' + response.text)
    return 'error - ' + response.text

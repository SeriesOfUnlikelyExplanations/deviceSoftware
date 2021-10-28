import pytest, requests_mock, subprocess, tarfile, os, json, shutil
from components.update import update
from components.cron import cron
from components.movies import movies
from components.updateip import updateip

#~@pytest.mark.skip(reason="this is how you skip tests")

with open('config.json', 'r') as config_file:
  data=config_file.read()
  config = json.loads(data)
print(config)

def test_ota(requests_mock):
  "Test the OTA"
  with tarfile.open('test/vanComputer.tar.gz', "w:gz") as tar:
    tar.add('.')
    tar.close()
  with open('test/vanComputer.tar.gz', 'rb') as f:
    requests_mock.get('https://www.always-onward.com/api/device/update', content=f.read(), status_code=200)
  result = update()
  assert result == 'Update Complete'
  os.remove("test/vanComputer.tar.gz")
  pass

def test_ota_not_needed(requests_mock):
  "Test the OTA when it's not needed"
  requests_mock.get('https://www.always-onward.com/api/device/update', text='', status_code=204)
  result = update()
  assert result == 'Software update not needed'
  pass

def test_cron_update(requests_mock):
  "Test cron update"
  result = cron()
  assert result == '@hourly bash '+os.getcwd()+'/cron.sh >> '+os.getcwd()+'/cron.log 2>&1 # vanComputer'
  result = cron()
  assert result == '@hourly bash '+os.getcwd()+'/cron.sh >> '+os.getcwd()+'/cron.log 2>&1 # vanComputer'
  # cleanup
  subprocess.run(['crontab', '-r'])
  pass

def test_update_ip(requests_mock):
  "Test updating IP address"
  requests_mock.post('https://www.always-onward.com/api/device/updateip', text='{"Id":"/change/C03973962VN4BRB0MCVPA","Status":"PENDING","SubmittedAt":"2021-08-20T14:06:06.160Z","Comment":"Routing for vanComputer"}')
  requests_mock.get('https://api.ipify.org/', text='8.8.8.8')
  result = updateip()
  assert result == '{"Id":"/change/C03973962VN4BRB0MCVPA","Status":"PENDING","SubmittedAt":"2021-08-20T14:06:06.160Z","Comment":"Routing for vanComputer"}'
  # cleanup
  subprocess.run(['crontab', '-r'])
  pass

def test_movies(requests_mock):
  "Test the movie download"
  # create files as prep-work
  os.mkdir(config['moviesDir'])
  open(config['moviesDir'] + '/movie1.mp4', 'a').close()

  requests_mock.get('https://www.always-onward.com/api/device/getmovie',
    text='{"status":"movieToDownload","name":"movie3.mp4","url":"https://www.signedUrl.com"}')

  requests_mock.get('https://www.signedUrl.com', content=b'Hello', status_code=200)
  result = movies()
  assert result == 'movie3.mp4 downloaded'
  assert os.path.exists(config['moviesDir'] + '/movie3.mp4')
  # cleanup
  shutil.rmtree(config['moviesDir'])
  pass

def test_movie_delete(requests_mock):
  "Test the movie download"
  # create files as prep-work)
  os.mkdir(config['moviesDir'])
  open(config['moviesDir'] + '/movie1.mp4', 'a').close()
  open(config['moviesDir'] + '/movie2.mp4', 'a').close()
  requests_mock.get('https://www.always-onward.com/api/device/getmovie',
    text='{"status":"movieToDelete","name":"movie2.mp4"}')

  result = movies()
  assert result == 'movie2.mp4 deleted'
  assert not os.path.exists(config['moviesDir'] + '/movie2.mp4')
  # cleanup
  shutil.rmtree(config['moviesDir'])
  pass

def test_no_movie(requests_mock):
  "Test no movies needed"
  # create files as prep-work
  os.mkdir(config['moviesDir'])
  open(config['moviesDir'] + '/movie1.mp4', 'a').close()

  requests_mock.get('https://www.always-onward.com/api/device/getmovie',
    text='', status_code=204)

  result = movies()
  assert result == 'Movies are up to Date'
  # cleanup
  shutil.rmtree(config['moviesDir'])
  pass

def test_movie_error(requests_mock):
  "Test response error"
  # create files as prep-work
  os.mkdir(config['moviesDir'])
  open(config['moviesDir'] + '/movie1.mp4', 'a').close()

  requests_mock.get('https://www.always-onward.com/api/device/getmovie',
    text='bad request', status_code=400)

  result = movies()
  assert result == 'error - bad request'
  # cleanup
  shutil.rmtree(config['moviesDir'])
  pass

#!/bin/bash
cd ~/service
export PATH="/usr/local/bin:/home/pi/.local/bin":$PATH

if ! command -v pipenv &> /dev/null; then
  #~ https://www.makeuseof.com/tag/install-kodi-raspbian-media-center/
  #~sudo apt-get install build-essential libssl-dev libffi-dev python3-dev python3-pip kodi x-window-system
  #~ sudo nano ~/.config/lxsession/LXDE-pi/autostart
  #~ @kodi
  pip3 install --upgrade pip
  pip3 install pipenv
fi

if [ -f "ota.log" ]; then
  echo "$(tail -10 ota.log)" > ota.log
fi
pipenv run python3 ota.py >> ~/service/ota.log 2>&1
PID=$!
wait $PID
if [ -f "main.log" ]; then
  echo "$(tail -10 main.log)" > main.log
fi
pipenv run python3 main.py >> ~/service/main.log 2>&1


if [ -f "cron.log" ]; then
  echo "$(tail -10 cron.log)" > cron.log
fi

echo "Cron successful - $(date)"

#~ scp -r vanComputer/ pi@192.168.0.30:/home/pi/service

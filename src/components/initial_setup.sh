sudo apt-get install build-essential libssl-dev libffi-dev python-dev python3-pip
pip3 install --upgrade pip
pip3 install pipenv
export CRYPTOGRAPHY_DONT_BUILD_RUST=1
pipenv install

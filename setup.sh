# Use this file when running the site off aws
git clone https://github.com/Etragas/waitforit.git
sudo apt-get update
sudo apt install python3-pip -y
sudo pip3 install -r waitforit/requirements.txt
# TODO Garmin Credentials
( cd waitforit; git pull; sudo python3 application.py ) &

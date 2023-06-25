# update machine
sudo apt-get update

#install apache to serve
sudo apt-get install libapache2-mod-wsgi-py3
sudo apt-get install apache2 libapache2-mod-wsgi

# web app goes in www
cd /var/www
sudo mkdir viberary

# Rsync from local machine
rsync --progress -e 'ssh -i /Users/vicki/droplet' -r /Users/vicki/viberary/viberary/src root@ip:/var/www/

sudo nano /etc/apache2/sites-available/viberary
sudo service apache2 restart

# Install docker
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt-cache policy docker-ce
sudo apt install docker-ce
sudo systemctl status docker

# set up app
docker compose build

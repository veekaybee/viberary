# update machine
sudo apt-get update

# web app goes in www
cd /var/www

# Add Github keys
# Sync with Github using key
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account

# Install nginx https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-20-04
sudo apt update
sudo apt install nginx

```
server {
    listen 80;
    server_name viberary.pizza staging.viberary.pizza;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/var/www/viberary.sock;
	      proxy_pass http://127.0.0.1:8000;
    }

}
`

# Install docker
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt-cache policy docker-ce
sudo apt install docker-ce
sudo systemctl status docker
sudo apt-get install docker-compose-plugin


# set up app
make build

#ssh over transformer model
scp
make up-intel
make embed

voila

# Metrics and alerting agent
curl -sSL https://repos.insights.digitalocean.com/install.sh | sudo bash
ps aux | grep do-agent

# Mount formatted volume for log backup
https://docs.digitalocean.com/products/volumes/how-to/mount/

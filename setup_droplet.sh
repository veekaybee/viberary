# update machine
sudo apt-get update


# web app goes in www
cd /var/www

# Sync with Github using key
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account


# Install nginx https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-20-04
sudo apt update
sudo apt install nginx

#
sudo vi /etc/nginx/sites-available/viberary
sudo systemctl reload nginx
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'
sudo nginx -s reload

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
```

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

# copy model
scp
make up-intel
make embed

# Set Up Certificate:
sudo vi /etc/nginx/sites-available/viberary
sudo ufw allow 443
sudo certbot certonly --standalone --preferred-challenges https -d viberary.pizza

# Metrics and alerting agent
curl -sSL https://repos.insights.digitalocean.com/install.sh | sudo bash
ps aux | grep do-agent

# Mount formatted volume for log backup
https://docs.digitalocean.com/products/volumes/how-to/mount/

# Where to find logs:
`cd /mnt/viberary`

# Back up logs to Spaces
```
sudo apt-get update && sudo apt-get install s3cmd
sudo apt-get install s3cmd
s3cmd --configure
s3cmd ls
s3cmd put mnt/viberary s3://viberary-beta
```

# Add Droplet to GH Actions for CI
```
https://github.com/veekaybee/viberary/blob/e07c72bcfa6fa4c23e9005761f8a19e18f6d8c57/.github/workflows/deploy.yml#L41
```

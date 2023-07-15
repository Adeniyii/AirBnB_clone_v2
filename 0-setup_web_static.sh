#!/usr/bin/env bash
# Script that sets up your web servers for the deployment of web_static

# install nginx
sudo apt-get update >/dev/null
sudo apt-get install nginx -y >/dev/null

#setup source directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
echo "Holberton School" >/data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/

new_string="\\\n\n\tlocation \/hbnb_static {\n\t\t alias /data/web_static/current/;\n\t\t try_files \$uri \$uri/ =404;\n\t}"
sudo sed -i "65i $new_string" /etc/nginx/sites-available/default

sudo service nginx start

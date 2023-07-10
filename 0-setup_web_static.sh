#!/usr/bin/env bash
# Script that sets up your web servers for the deployment of web_static

# install nginx
sudo apt update
sudo apt install nginx -y

#setup source directories
mkdir -P /data/web_static/releases/test/
mkdir -P /data/web_static/shared/
echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/

new_string="\\\n\n\tlocation \/hbnb_static {\n\t\t alias /data/web_static/current/;\n\t\t try_files \$uri \$uri/ =404;\n\t}"
sudo sed -i "65i $new_string" /etc/nginx/sites-available/default

# sudo touch /etc/nginx/sites-available/airbnb
# sudo sed -i "54i $new_string" /etc/nginx/sites-available/airbnb
# sudo ln -s /etc/nginx/sites-available/airbnb /etc/nginx/sites-enabled/airbnb

sudo service nginx start

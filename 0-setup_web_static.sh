#!/usr/bin/env bash
#sets up your web servers for the deployment of web_static
#Install Nginx if it not already installed
#Create the folder /data/ if it doesn’t already exist
#Create the folder /data/web_static/ if it doesn’t already exist
#Create the folder /data/web_static/releases/ if it doesn’t already exist
#Create the folder /data/web_static/shared/ if it doesn’t already exist
#Create the folder /data/web_static/releases/test/ if it doesn’t already exist
#Create a fake HTML file /data/web_static/releases/test/index.html
#Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder
#Give ownership of the /data/ folder to the ubuntu user AND group (you can assume this user and group exist)

# Update package lists and install Nginx
apt-get update
apt-get install -y nginx

# Create necessary folders (if they don't exist)
mkdir -p /data/{web_static,web_static/releases/test,web_static/shared}
# Create a fake HTML file for testing
echo "Holberton School" > /data/web_static/releases/test/index.html
# Create/update symbolic link to current release
rm -f /data/web_static/current && ln -s /data/web_static/releases/test /data/web_static/current
# Set ownership of the /data directory recursively
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration file using a heredoc
cat << EOF > /etc/nginx/sites-available/default
server {
  listen 80 default_server;
  listen [::]:80 default_server;  # Add IPv6 support
  add_header X-Served-By $HOSTNAME;

  root /data/web_static/current;
  index index.html index.htm;

  location /hbnb_static {
    alias /data/web_static/current/;
    index index.html index.htm;
  }

  # Add a redirect example
  location /redirect_me {
    return 301 http://cuberule.com/;
  }

  # Add a custom 404 page configuration
  error_page 404 /404.html;
  location /404 {
    root /var/www/html;
    internal;
  }
}
EOF

# Enable the default server block and restart Nginx
ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
service nginx restart

echo "Nginx is installed and configured!"

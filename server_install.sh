#!/bin/bash

apt update
apt install git nginx python3 python3-pip python3-venv python3-dev -y

useradd -m toto
su - toto -c "git clone https://github.com/ldsvrn/SAE301 /home/toto/django"
chmod 774 /home/toto/django/user_install.sh

su - toto -c '/home/toto/django/user_install.sh'

cat << EOS > /etc/systemd/system/gunicorn.socket
[Unit]
Description=gunicorn socket
[Socket]
ListenStream=/run/gunicorn.sock
[Install]
WantedBy=sockets.target
EOS

cat << EOF > /etc/systemd/system/gunicorn.service
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target
[Service]
User=toto
Group=www-data
WorkingDirectory=/home/toto/django/django
ExecStart=/home/toto/django/django/sae301/.venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock sae301.wsgi:application
[Install]
WantedBy=multi-user.target
EOF

systemctl start gunicorn.socket
systemctl enable gunicorn.socket

cat << EOF > /etc/nginx/sites-available/sae301
server {
    listen 80;
    server_name mqtt.louis.systems;
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/toto/django/django/sae301;
    }
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOF

ln -s /etc/nginx/sites-available/sae301 /etc/nginx/sites-enabled/

systemctl restart nginx

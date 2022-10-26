#!/bin/bash

apt update
apt install git nginx python3 python3-pip python3-venv python3-dev -y

useradd -m toto
su - toto -c "git clone https://github.com/ldsvrn/SAE301 /home/toto/django"
chmod 774 /home/toto/django/user_install.sh
echo "192.168.69.2 mqtt.louis.systems" >> /etc/hosts

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
WorkingDirectory=/home/toto/django/django/sae301
ExecStart=/home/toto/django/django/sae301/.venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock sae301.wsgi:application
[Install]
WantedBy=multi-user.target
EOF

systemctl start gunicorn.socket
systemctl enable gunicorn.socket

cat << EOF > /etc/nginx/sites-available/mqtt.louis.systems
server {
    listen 80;
    server_name mqtt.louis.systems;
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static {
        root /var/www/;
    }
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOF

ln -s /etc/nginx/sites-available/mqtt.louis.systems /etc/nginx/sites-enabled/

cp -r /home/toto/django/django/sae301/static /var/www/static
chown -R www-data:www-data /var/www/static
# flemme de chercher la soluce donc lets go osef le serv tournera pas longtemps
chmod -R 777 /var/www/static

systemctl restart nginx

apt install certbot python3-certbot-nginx

certbot --nginx -d mqtt.louis.systems --register-unsafely-without-email -n
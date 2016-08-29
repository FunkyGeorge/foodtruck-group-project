# Set up instance
* sudo apt-get update
* sudo apt-get upgrade
* sudo apt-get install python-pip python-dev nginx git build-essential libffi-dev
* sudo apt-get install libmysqlclient-dev
* sudo apt-get install uwsgi
* sudo pip install virtualenv
* sudo apt-get install mysql-server


# Set up project
* git clone -b development <repo>
* python setup.py
* check that (virtualenv) is active
* (root) mysql> CREATE DATABASE myproject;
* (root) mysql -u root -p myproject < myproject.sql
* mysql -u root -p
* mysql> show databases;
* mysql> use myproject;
* mysql> show tables;
* leave root
* check database.py
* test server .py files:
* (venv) python manage.py runserver
* (venv) python wsgi.py
* deactivate to leave venv
* edit and rename wsgi-project.ini
* sudo vi /etc/init/<project>.conf
* ``` description "uWSGI server instance configured to serve myproject"
start on runlevel [2345]
stop on runlevel [!2345]
setuid root
setgid www-data
env PATH=/home/ubuntu/<myproject>/venv/bin
chdir /home/ubuntu/<myproject>
exec uwsgi --ini <myproject>.ini ```
* init-checkconf -d /etc/init/<service_name>.conf
* sudo start <myproject>
* sudo nano /etc/nginx/sites-available/<myproject>
* ``` server {
    listen 80;
    server_name YOUR_AWS_IP/DOMAIN NAME;
    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/ubuntu/myproject/<myproject>.sock;
    }
}```
* sudo ln -s /etc/nginx/sites-available/<myproject> /etc/nginx/sites-enabled
* sudo nginx -t
* sudo rm /etc/nginx/sites-enabled/default
* sudo service nginx restart

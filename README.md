newsletter_archive
==================

Repository for newsletter archive project.


How to setup

1. Get source code 
    cd ~; mkdir www;
    cd www
    git clone https://github.com/victorliun/newsletter_archive.git

2. check up dependences:
    sudo apt-get update 
    sudo apt-get install git
    sudo apt-get install nginx
    sudo apt-get install virtualenv
    sudo apt-get install python-virtualenv
    sudo apt-get install nodejs
    sudo apt-get install npm
    sudo apt-get install phantomjs
    sudo apt-get install rabbitmq-server
    sudo apt-get install mysql-server
    sudo apt-get install python-mysqldb
    sudo apt-get install mysql_config
    sudo apt-get install libmysqlclient-dev
    sudo apt-get install libmysqlclient-dev
    sudo apt-get install python-dev
    sudo apt-get install libxml2-dev
    sudo apt-get install libxslt1-dev
    sudo apt-get install mongodb

3. install environment
    virtualenv env
    ln -s env/bin/activate
    source activate
    pip install -r requirements.text —download-cache=~/.pip-cache
    mysql.server start
    ./manage.py syncdb
    ./manage.py schemamigration archive --auto --update
    ./manage.py migrate archive 
    ./manage.py migrate
    ./manage.py runserver # go to localhost:8000 test

4.  config server:
    # change settings in uwsgi.ini
    ln -s serverconf/newsletter_archive.conf /usr/local/etc/nginx/sites-available/ 
    nginx #start nginx
    rabbitmq-server start #start mq

5. Commands:
    #run celery
    cd newsletter_archive/project
    ./manage.py celery worker
    ./manage.py celerybeat
    ./manage.py help

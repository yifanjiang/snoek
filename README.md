Time-stamp: "2014-07-18 16:49:49 yifan"

## Contacts

Please read aloud to fetch the email:

* yifanj2007 AT gmail DOT com
* yfjiang AT suse DOT com

## Development Guide

### Get the code

You can retrieve the code by cloning this repo:

    git@github.com:yifanjiang/snoek.git

### Prerequisite

* Python>=2.6 (core python)
* Django==1.2.4 (python module)
* Odfpy==0.9.2 (python module)
* celery==2.5.3 (python module)
* django-celery==2.5.5 (python module)
* kombu==2.1.8 (python module)
* A static http server (Apache, lighttp, etc.)

*Notice:* It is highly suggested to use 'pip install' to install python modules.

### Hosting static content

Link the static content (css, image) to the root of your http server.

    snoek/$ sudo ln -s $(readlink -f ./media) $your_static_http_root

The following is an example of my development environment. The static
http root is in /srv/www/htdoc

    $ find /srv/www/htdocs/ -maxdepth 1 -type l | xargs ls -l
    lrwxrwxrwx 1 root root 32 2012-07-30 13:28 /srv/www/htdocs/media -> /home/yifan/project/snoek/media/

### Create settings.py


1. Make a Copy settings.py.sample

        snoek/$ cp settings.py.sample .

2. To edit settings.py for your own testing environment, usually you
only need to modify the MEDIA_URL value:

        MEDIA_URL = 'http://localhost/media/'

to make it point to your static server's root URL. This makes the css,
image, jquery canbe imported to Snoek.

### Create database

It is fairly simple to start a new empty database in snoek:

    snoek/$ python manage.py syncdb

*Notice:* you will be asked to set a super user's password of the
database.

Meanwhile we also provide a sample database with test data populated
for your experiments, to make use of it, simple make a copy:

    snoek/$ cp db.sqlite.sample db.sqlite

### Run testing server

   snoek/$ python manage.py runserver celyryd # this is particularly for library module, not necessarily used in the voting system.
   
   snoek/$ python manage.py runserver localhost:8080

### Play snoek

1. Open you browser and visit the url http://localhost:8080/admin

Login with the super user you set in the "Create database" section and
try to create several users in the adminitration pages.

2. Open you browser and visit the url http://localhost:8080

Normally you can play with Snoek now!

### Patch submission

Let's just use any of the ordinary processes:

1. Send a Pull Request from github

2. Send a patch by email using `git format-patch` 

## Usage

### Activities

1. Login the web site and click an activity you are interested in

2. Attend the vote by clicking Take Vote section

    * You could only have one chance of voting at the moment

    * You will not be able to vote for an activity if it is outdated

3. The statistics of votings are shown in the section Voting Results

    * If only one vote is in the activity, there will be only one table to describe the results

    * If multiple votes are created in the activity, multiple tables would be generated to describe:

        - one dimension data for each votes

        - two dimension data for for possible combinations of any two of the votes

    * All voters' favourite choice can be found by clicking 'Who vote what' link

    * The ODF format of voting results can be downloaded by click 'Download me'

    * You may change your password by clicking the tiny icon beside the user name

### Library

USAGE:

    1. first add book reader in http://site/admin/ to ad a book reader

    2. choose book reader in EDIT

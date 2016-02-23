[![Coverage Status](https://coveralls.io/repos/github/andela-egichuri/checkpoint4/badge.svg?branch=develop)](https://coveralls.io/github/andela-egichuri/checkpoint4?branch=develop) [![Build Status](https://travis-ci.org/andela-egichuri/checkpoint4.svg?branch=develop)](https://travis-ci.org/andela-egichuri/checkpoint4) [![Code Issues](https://www.quantifiedcode.com/api/v1/project/85cca79685584a9ca2dac184ebbfbf60/snapshot/origin:develop:HEAD/badge.svg)](https://www.quantifiedcode.com/app/project/85cca79685584a9ca2dac184ebbfbf60)
## PicMate
### Application Overview
Picmate is a Django powered photo editing application. It allows a user to perform a set of filters and effects on images he uploads.
A user can register or login using either Facebook or Twitter.

 - Framework in use: [Django](https://www.djangoproject.com/)
 - Authentication: [Django Allauth](https://github.com/pennersr/django-allauth)
 - Image Manipulation: [Pillow](http://python-pillow.org/)
 - Image Upload: [ImageKit](https://github.com/matthewwithanm/django-imagekit)

### Installation

Install Python on your system

Install a relational database (Postgres has been used for development and testing).

Download or clone the repo

 * Install requirements.
`pip install -r requirements.txt`
 * Setup environment variables
`DATABASE_URL="postgres://<user>:<password>@localhost:5432/<db_name>"`
`SECRET=<SECRET>`

 * Perform database migrations.
`python manage.py makemigrations`
`python manage.py migrate`

 * Run the application
`python manage.py runserver`

 * Create the admin user
 ` python manage.py createsuperuser`
 * Login as admin and configure social authentication apps. For this you need to:

     * Add a Site for the domain in use, matching settings.SITE_ID (django.contrib.sites app).
     * Create Facebook and Twitter apps to get provider credentials.
 * Add effects and filters. The ones configured are listed below.

|Effect Type  | Effect  |
|---|---|
|image | rotate|
|imageenhance | enhance |
|imagefilter | smooth, emboss, contour, sharpen, findedges, blur|
|imageops | flip, mirror, grayscale |
Log in on the main site to upload images and apply effects and filters

### Testing
Tests are configured to to use `nosetests`. This is done from the root folder
`python manage.py test`

To show Coverage results
`coverage report -m`

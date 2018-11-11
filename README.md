# Django-Scrapy

1- install python 3.6.5

2- open terminal in scrapy/onlineshopping

3- install virtualenv -->$ sudo pip3 install virtualenv
	
4- activate virtualenv --> $ source env/bin/activate

5- install dependencies --> $pip install -r requirements.txt

6- Create mysql database 'shopping'

7- change username and password in file onlineshopping/settings.py in DATABASES section with your mysql user and password

8- apply migrations $ ./manage.py migrate

9- Run project $ ./manage.py runserver

10- open another terminal in scrapy/onlineshopping

11- $celery -A onlineshopping.celery worker -B -l info -E
** this will run scrapy every 30 seconds (we could change it to run daily instead) **

12- start Front End 


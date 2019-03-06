IVR Homework (Miguel Mendez)
==================================

How to start.
-----------

In this project I worked with MySql. So:
 
- You need to create an database called 'ivr'
- Create an user and password with all the privileges 
('miguelmendez' and 'm1gu3l123.' respectively) 

Or you can use your own configurations, but you need to change this in settings.py

How to run the project
------------


Before start install requirements and run migrations:

    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate

We need to create a super user:

    python manage.py createsuperuser
    
Here, we need to define an username, email (optional) and password.

To run
--------

    python manage.py runserver
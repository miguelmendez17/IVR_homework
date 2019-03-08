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
    

How to use the application
-----

This is a web service, so in this project you can post the Card information associated
with a payment. You have to send Card information and payment information, you have to
send a correct data or you will get a response with the corresponding error in case
that any data fails. 

The correct way to send the post is similar to this form:

    curl -d '{"cc_num":"4111111111111111", "cvc":"123", "exp_month":12, "exp_year":2020,
    "amount":100, "description":"This is a charge."}' 
    -H "Content-Type: application/json" -X POST http://localhost:8000
    
The stripe api verifies that the data is correct, otherwise the system is able to 
send the corresponding error.
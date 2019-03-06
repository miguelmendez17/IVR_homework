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
    python manage.py migrate

Try to import the registry.

Download from http://www.tse.go.cr/zip/padron/padron_completo.zip the complete registry file
Unzip the file and run

:warning:   Do not open the file 'PADRON_ELECTORAL_COMPLETO.txt', computer could freeze.

::

   python manage.py  importregistry  <registry path> <diselect path>




To run
--------

::

   python manage.py runserver
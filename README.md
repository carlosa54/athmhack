### Python

For this project you will need python 2.7.x installed on your computer.
You can download the python installer [here.](https://www.python.org/downloads/)

**Note: Depending on your Operating system, you may have python already installed.**

To check if you have python installed, you can try the following in the command line.

```bash
$ python
```

This will get you to the python shell and it also provides the python version that's installed.

#### Virtual Environment

This is not necessary, but it is highly recommended. A virtual environment is a place where
you can work separately from your global environment and install everything you want and never
affect your global environment.

To do this in python, you can install `virtualenv` with `easy_install` or `pip`. We recommend `pip`.

```bash
$ pip install virtualenv
```

To create a `virtualenv`, select a folder where you want to work with the project and do the following:
 
```bash
$ virtualenv venv
```

That will create a virtual environment for python. To activate it do the following:

```bash
$ source venv/scripts/activate
```

#### Dependencies

**Before installing the python dependencies, you will need to install postgresql
 and add the bin path to your environment.**

#### Windows Environment Only

Fist execute this command in order to install psycopg2 for windows

```bash
$ easy_install http://www.stickpeople.com/projects/python/win-psycopg/2.6.1/psycopg2-2.6.1.win32-py2.7-pg9.4.4-release.exe
```

#### Every OS
Now that you are in your venv, let's take care of project dependencies.

In the command line, go to the projects root folder and do the following:

```bash
$ pip install -r requirements.txt
```

#### Environment

This project uses environment variables to keep secret settings secret. To get started, you would need to copy the `example.env` file to a new file called `.env` in the same directory.

```bash
$ cp example.env .env
```

#### Database Migrations

```bash
$ python manage.py migrate
```

#### Create a superuser

```bash
$ python manage.py createsuperuser
```

#### Running the project

```bash
$ python manage.py runserver_plus
```

#### Django Admin Interface

Go to `http://localhost:8000/admin` in your browser and enter your credentials.
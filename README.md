# CoSo : Comportement Sondage 

CoSo is a software that analyzes the behaviour of different polls regarding political elections. It is implemented in Django (version 1.10).

## 1. Git commands :

### To get last modifications :
`$ cd ~/CoSo`
`$ git pull`

### To create a new branch from master
`$ git checkout master`
`$ it fetch`
`$ git pull` (to get the last version of master)
`$ git branch _name-of-the-branch_`
`$ git checkout _name-of-the-branch_`

### To add your modifications
`$ cd ~/CoSo`
`$ git add .`
`$ git status`
`$ git commit -m "message detailing the modifications"`
`$ git push`

In order to write some git commit messages, we will follow the rules from http://chris.beams.io/posts/git-commit/

## 2. Setting up the development environment with virtualenv

virtualenv is a tool to create isolated Python environments. virtualenv creates a folder which contains all the necessary executables to use the packages that a Python project would need.

### 2.1. Installation

Install virtualenv via pip:
`$ pip install virtualenv`

Basic Usage - Create a virtual environment for a project:
`$ cd my_project_folder`
`$ virtualenv ENV`
virtualenv ENV will create a folder in the current directory which will contain the Python executable files, and a copy of the pip library which you can use to install other packages. The name of the virtual environment (in this case, it was ENV) can be anything; omitting the name will place the files in the current directory instead.

This creates a copy of Python in whichever directory you ran the command in, placing it in a folder named ENV.

### 2.2. Usage of the virtual environment

To begin using the virtual environment, it needs to be activated (everytime the project is being run):
`$ source ENV/bin/activate`
The name of the current virtual environment will now appear on the left of the prompt (e.g. (ENV)Your-Computer:your_project UserName$) to let you know that it’s active. From now on, any package that you install using pip will be placed in the ENV folder, isolated from the global Python installation.

Install packages as usual, for example:

`$ pip install -r requirements.txt`
If you are done working in the virtual environment for the moment, you can deactivate it:
`$ deactivate`

Find more at : http://docs.python-guide.org/en/latest/dev/virtualenvs/

### 2.3. Requirements files

"Requirements files" are files containing a list of items to be installed using pip install like so:

`$ pip install -r requirements.txt`

Requirements File Format:

Logically, a Requirements file is just a list of pip install arguments placed in a file. Note that you should not rely on the items in the file being installed by pip in any particular order.

Requirements files are used to hold the result from pip freeze for the purpose of achieving repeatable installations (for example when sharing code on a project). In this case, your requirement file contains a pinned version of everything that was installed when pip freeze was run.

How to add a new item to be installed for the project :

`$ pip install package1`
`$ pip freeze`

Requirements files are used to force pip to properly resolve dependencies.

Find more at : https://pip.pypa.io/en/stable/user_guide/

## 3. The development server (to run the Backend)

To verify that Django project works : change into the outer coso directory `$ cd coso/`, if you haven’t already, and run the following commands:

`$ python manage.py runserver`
You’ll see the following output on the command line:

```
November 25, 2016 - 15:50:53
Django version 1.10, using settings 'coso.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
Now that the server’s running, visit http://127.0.0.1:8000/polls with your Web browser.

## 3. Django project organisation

coso/
    coso/
        __init__.py
        settings.py
        urls.py
        wsgi.py
    polls/
    	__init__.py
    	admin.py
    	apps.py
    	migrations/
        	__init__.py
    	models.py
    	tests.py
    	views.py
    manage.py


These files were automatically created by Django, they are:

coso/ : root directory is just a container for your project.
manage.py: A command-line utility that lets you interact with this Django project in various ways. coso/coso/ directory is the actual Python package for your project. Its name is the Python package name you’ll need to use to import anything inside it (e.g. coso.urls).
coso/__init__.py: An empty file that tells Python that this directory should be considered a Python package.
coso/settings.py: Settings/configuration for this Django project. Django settings will tell you all about how settings work.
coso/urls.py: The URL declarations for this Django project; a “table of contents” of your Django-powered site. You can read more about URLs in URL dispatcher.
mysite/wsgi.py: An entry-point for WSGI-compatible web servers to serve your project.

## 4. Database

### 4.1. Setting up the database

Pre-installed:
- mysql

1. Create a database called 'coso'
2. type `python manage.py migrate`

### 4.2. How to add a new class to the database or modify an existing one

1. Make the changes in models.py
2. For example, if the changes are in the polls app : `$ python manage.py makemigrations polls`
3. You should see a new file in polls/migrations: polls/migrations/000x.py
4. To apply the migration to the Database : `$ python manage.py migrate`

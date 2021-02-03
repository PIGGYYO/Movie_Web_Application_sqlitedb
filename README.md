# Movie Web Application

## Description

A Web application that makes use of Flask configuration, Jinja templating, WTForms and blueprints. 

## Installation

**Installation via requirements.txt**

```shell
$ cd Movie_Web_Applicatio_sqlitedb
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select 'Project:Movie_Web_Application_sqlitedb' from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

## Configuration

The Movie_Web_Application_sqlitedb/.env file contains variable settings. They are set with appropriate values.

FLASK_APP: Entry point of the application (should always be wsgi.py).
FLASK_ENV: The environment in which to run the application (either development or production).
SECRET_KEY: Secret key used to encrypt session data.
TESTING: Set to False for running the application. Overridden and set to True automatically when testing the application.
WTF_CSRF_SECRET_KEY: Secret key used by the WTForm library.

## Execution

**Running the application**

From the *Movie_Web_Application_sqlitedb* directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

The homepage can be accessed from a Web browser:

http://127.0.0.1:5000/


## Testing

Testing requires that file *Movie_Web_Application_sqlitedb/tests/conftest.py* be edited to set the value of `TEST_DATA_PATH`. You should set this to the absolute path of the *Movie_Web_Application_sqlitedb/tests/data* directory. 

You can then run tests from within PyCharm.

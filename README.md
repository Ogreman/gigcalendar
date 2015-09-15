# gigcalendar

Installation
------------

Recommend using [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/).

    $ git clone git@github.com:Ogreman/gigcalendar.git
    $ cd gigcalendar
    $ pip install -r requirements.txt

Get google secret file from [developer console](https://console.developers.google.com/).


Usage
-----

To run the webserver locally on port 5000:

    $ cd gigcalendar
    $ python app.py


Environment Variables & Virtual Environments
--------------------------------------------

With virtualenvwrapper installed, it is recommended to add the following to the activation hooks:

    $ mkvirtualenv gig-env
    $ cd $VIRTUAL_ENV/bin
    
    $ echo export APP_TOKEN_A="MY_SLACK_INTEGRATION_TOKEN_FOR_CREATE" >> postactivate
    $ echo export APP_TOKEN_B="MY_SLACK_INTEGRATION_TOKEN_FOR_LIST" >> postactivate
    $ echo export GOOGLE_SCOPE="MY_GOOGLE_SCOPE_URL" >> postactivate
    $ echo export GOOGLE_SECRET_FILE="NAME_OF_SECRET_FILE" >> postactivate
    $ echo export BRISTOL_CALENDAR="BRISTOL_CALENDAR_ID" >> postactivate
    $ echo export NOTTS_CALENDAR="NOTTS_CALENDAR_ID" >> postactivate
    
    $ echo unset APP_TOKEN_A >> postdeactivate
    $ echo unset APP_TOKEN_B >> postdeactivate
    $ echo unset GOOGLE_SCOPE >> postdeactivate
    $ echo unset GOOGLE_SECRET_FILE >> postdeactivate
    $ echo unset BRISTOL_CALENDAR >> postdeactivate
    $ echo unset NOTTS_CALENDAR >> postdeactivate
    
    $ deactivate
    $ workon gig-env
    $ echo $NOTTS_CALENDAR
    NOTTS_CALENDAR_ID

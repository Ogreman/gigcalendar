import os
import oauth2client
from oauth2client import client
from oauth2client import tools
from apiclient import discovery
import httplib2

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gigs Calendar'
API_KEY = 'AIzaSyDtBGVFvMk3LRxPytNmB2z0gTUs4d077Qw'


CALENDARS = {
    'bristol': '8bog3m0l9cfgt48cbk3lgdk8o0@group.calendar.google.com',
    'notts': '1gghroldtmjh8mvuo63s33r2uk@group.calendar.google.com',
}


# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None


class Flag(object):        
    auth_host_name='localhost' 
    auth_host_port=[8080, 8090] 
    logging_level='ERROR' 
    noauth_local_webserver=True
flags = Flag()


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ' + credential_path
    return credentials


def create_event(credentials, calendar, event):
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http, developerKey=API_KEY)

    for k, v in event.items():
        if isinstance(v, dict):
            for kk, vv in v.items():
                event[k][kk] = vv.strip()
        else:
            event[k] = v.strip()

    eventsResult = service.events().insert(
        calendarId=CALENDARS[calendar.strip().lower()], 
        body=event
    ).execute()
    return eventsResult.get('htmlLink')


def list_events(credentials, calendar, date):
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http, developerKey=API_KEY)

    start = '{date}T00:00:00+01:00'.format(date=date.strip())
    end = '{date}T23:59:59+01:00'.format(date=date.strip())

    eventsResult = service.events().list(
        calendarId=CALENDARS[calendar.strip().lower()], 
        timeMin=str(start), timeMax=str(end), 
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    return eventsResult.get('items', [])
    
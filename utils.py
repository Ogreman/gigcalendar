import os
import datetime
import oauth2client
from oauth2client import client
from oauth2client import tools
from apiclient import discovery
import httplib2


SCOPES = os.environ.get('GOOGLE_SCOPE')
CLIENT_SECRET_FILE = os.environ.get('GOOGLE_SECRET_FILE')
APPLICATION_NAME = 'Gigs Calendar'
CALENDARS = {
    key.split('_')[0].lower(): value
    for key, value in os.environ.items()
    if key.endswith('_CALENDAR')
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
    service = discovery.build('calendar', 'v3', http=http)
    conform_dict(event, sort_string)
    eventsResult = service.events().insert(
        calendarId=CALENDARS[calendar.strip().lower()], 
        body=event
    ).execute()
    return eventsResult.get('htmlLink')


def conform_dict(d, func=str.strip):
    for k, v in d.items():
        if isinstance(v, dict):
            for kk, vv in v.items():
                d[k][kk] = func(vv)
        else:
            d[k] = func(v)


def sort_string(val):
    """Transforms a UK date (DD-MM-YYYY) string
    to US (YYYY-MM-DD) for Google API.

    Returns:
        transormed and whitespace-stripped string"""
    val = val.strip()
    if '-' in val:
        parts = val.split('-')
        if len(parts[2]) > 2:
            parts.reverse()
            val = '-'.join(parts)
    elif val == 'today':
        val = datetime.date.today().isoformat()
    return val


def list_events(credentials, calendar, date):
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    date = sort_string(date)

    start = '{date}T00:00:00+01:00'.format(date=date)
    end = '{date}T23:59:59+01:00'.format(date=date)

    eventsResult = service.events().list(
        calendarId=CALENDARS[calendar.strip().lower()], 
        timeMin=str(start), timeMax=str(end), 
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    return eventsResult.get('items', [])
    
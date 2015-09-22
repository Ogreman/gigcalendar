import os
import logging
from utils import create_event, get_credentials, list_events, quick_create_event
from flask import Flask, request, jsonify
from apiclient.http import HttpError

FORMAT = "%(asctime)-15s: %(levelname)s: %(message)s"
logging.basicConfig(format=FORMAT, filename="gigs.log", level=logging.INFO)

app = Flask(__name__)
app.google_credentials = get_credentials()

APP_TOKENS = [
    val
    for key, val in os.environ.items()
    if key.startswith('APP_TOKEN')
]
CALENDARS = ['bristol', 'notts']

event = {
  'summary': 'Test',
  'start': {
    'date': '2015-09-14'
  },
  'end': {
    'date': '2015-09-15'
  }
}


def add_gig(calendar, text):
    try:
        return "Gig added! <{result}|Click here> for details!".format(
            result=quick_create_event(
                app.google_credentials, 
                calendar, 
                text
            )
        )
    except HttpError as e:
        logging.exception(str(e))
        return "Failed to add gig :( Check calendar permissions."


def list_gigs(calendar, date):
    try:
        events = list_events(app.google_credentials, calendar, date)
        return '\n'.join(
            [
                "<{0}|{1} @ {2}>"
                .format(
                    event.get('htmlLink'),
                    event['summary'],
                    event.get('location', calendar.title())
                )
                for event in events
            ]
        ) or 'No events!'
    except HttpError as e:
        logging.exception(str(e))
        return "Failed to list gigs :( Check calendar permissions."


@app.route("/")
def index():
    return 'doom'


@app.route("/gig", methods=['POST'])
def create():
    
    def get_args(request, func_name):
        return request.form['text'][len(func_name) + 1:].split(',')

    def get_func(func_name):
        return {
            'add': add_gig,
            'list': list_gigs,
        }[func_name]

    def get_fname(request):
        return request.form['text'].split(' ')[0]

    if request.form.get('token') in APP_TOKENS:
        try:
            fname = get_fname(request)
            function = get_func(fname)
            calendar, arg = get_args(request, fname)
            if calendar.lower() in CALENDARS:
                return function(calendar, arg)
            else:
                return "Invalid calendar"
        except (ValueError, KeyError) as e:
            logging.exception(str(e))
            return "Error - requires three values ([option] [calendar], text)"
    else:
        logging.error("invalid token: %s", request.form.get('token'))
    return "Nope :|"


if __name__ == "__main__":
    app.run(debug=os.environ.get('GIG_DEBUG', True))



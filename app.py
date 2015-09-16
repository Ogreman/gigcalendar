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


event = {
  'summary': 'Test',
  'start': {
    'date': '2015-09-14'
  },
  'end': {
    'date': '2015-09-15'
  }
}


@app.route("/")
def index():
    return 'doom'


@app.route("/create", methods=['POST'])
def create():
    if request.form.get('token') in APP_TOKENS:
        try:
            calendar, text = request.form['text'].split(',')
        except (ValueError, KeyError) as e:
            logging.exception(str(e))
            return "Error - requires two values (calendar and text)"
        if calendar.lower() in ['bristol', 'notts']:
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
    else:
        logging.error("invalid token: %s", request.form.get('token'))
    return "Nope :|"


@app.route("/list", methods=['POST'])
def list():
    if request.form.get('token') in APP_TOKENS:
        try:
            calendar, date = request.form['text'].split(',')
        except (ValueError, KeyError) as e:
            logging.exception(str(e))
            return "Error - requires two values (calendar name and date)"
        if calendar.lower() in ['bristol', 'notts']:
            try:
                events = list_events(app.google_credentials, calendar, date)
                return '\n'.join(
                    [
                        "{0}, {1}"
                        .format(
                            event['start'].get(get('date')), 
                            event['summary']
                        )
                        for event in events
                    ]
                ) or 'No events!'
            except HttpError as e:
                logging.exception(str(e))
                return "Failed to list gigs :( Check calendar permissions."
    else:
        logging.error("invalid token: %s", request.form.get('token'))
    return "Nope :|"



if __name__ == "__main__":
    app.run(debug=os.environ.get('GIG_DEBUG', False))



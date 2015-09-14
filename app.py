from utils import create_event, get_credentials, list_events
from flask import Flask, request, jsonify
from apiclient.http import HttpError

app = Flask(__name__)
app.google_credentials = get_credentials()


APP_TOKENS = ["9u4Vj53UwTsSDxBxSPHkrTfJ", "nO5v58iT7qKgXJTqXc3zSEYt"]


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
    return ''


@app.route("/create", methods=['POST'])
def create():
    if request.form['token'] in APP_TOKENS:
        try:
            calendar, event['summary'], event['start']['date'], event['end']['date'] = request.form['text'].split(',')
        except ValueError:
            return "Error - requires three values"
        
        if calendar.lower() in ['bristol', 'notts']:
            if calendar.lower() == 'notts':
                return "Notts calendar not yet ready."
            try:
                return "Gig added! <{result}|Click here> for details!".format(
                    result=create_event(calendar, event)
                )
            except HttpError as e:
                print e
                return "Failed to add gig :( Check calendar permissions."
    return "Nope :|"


@app.route("/list", methods=['POST'])
def list():
    if request.form['token'] in APP_TOKENS:
        try:
            calendar, date = request.form['text'].split(',')
        except ValueError:
            return "Error - requires two values (calendar name and date)"
        if calendar.lower() in ['bristol', 'notts']:
            try:
                events = list_events(calendar, date)
                return '\n'.join(
                    [
                        "{0}, {1}".format(event['start'].get('dateTime', event['start'].get('date')), event['summary'])
                        for event in events
                    ]
                ) or 'No events!'
            except HttpError as e:
                print e
                return "Failed to list gigs :( Check calendar permissions."
    return "Nope :|"



if __name__ == "__main__":
    app.run(debug=True)



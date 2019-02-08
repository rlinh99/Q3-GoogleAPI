from __future__ import print_function

from flask import Flask

from events_handler import get_events, create_event

app = Flask(__name__)


@app.route("/")
def home():
    events = get_events()
    event_str = ""
    for event in events:
        event_str += "<h3>" + event + "</h3>"
    return event_str + "<a href='/create'>Create Even</a>"


@app.route("/create")
def create():
    create_event()
    return "Event is created"


if __name__ == "__main__":
    app.run(debug=True)

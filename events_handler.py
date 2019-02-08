from __future__ import print_function

import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import discovery


# function for retrieving all events
def get_events():
    # code retrieved from google api example
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting all upcoming events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=2500, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    event_records = []
    for event in events:
        start = event['start'].get('dateTime').replace("T", " ")
        end = event['end'].get('dateTime').replace("T", " ")
        summary = event['summary']
        print(type(start))
        event_str = "Event {0} starts at {1}, ends at {2}".format(summary, start, end)
        event_records.append(event_str)

    return event_records


def create_event():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = discovery.build('calendar', 'v3', credentials=creds)

    event = {
        'summary': 'Meeting - Speaker: Prof. Michael Collins',
        'location': 'Simon Fraser University, 8888 University Drive, Burnaby, BC, V5A 1S6',
        'description': 'It is a meeting',
        'start': {
            'dateTime': '2019-02-06T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'organizer': {
            'email': 'Michael_Collins@test123.com',
            'displayName': 'Prof. Michael Collins',
        },
        'end': {
            'dateTime': '2019-02-06T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
        'attendees': [{
            'displayName': 'Prof. Michael Collins',
            'email': 'Michael_Collins@test123.com'
        }],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    print("asdasd")

    event = service.events().insert(calendarId='primary', body=event).execute()
    print("asdasd")
    print('Event created: %s' % (event.get('htmlLink')))

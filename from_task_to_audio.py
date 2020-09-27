from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pyttsx3


def get_tasks_from_calendar():
    # source: https://developers.google.com/calendar/quickstart/python
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
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
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    tasks = events_result.get('items', [])
    task_list = []
    if not tasks:
        print('No upcoming tasks found.')
    for event in tasks:
        today = str(datetime.date.today())
        task_date = event['start'].get('dateTime', event['start'].get('date'))
        if today in task_date:
            task_list.append(event["summary"])

    return task_list



def say_tasks(tasks,name):
    speaker = pyttsx3.init() # Initializing the speaker
    voices = speaker.getProperty("voices") # Getting the available voices
    speaker.setProperty("voice",voices[1].id) # Setting a nicer voice than default
    speaker.say("Good Morning Lucas, your tasks for today are:") # Introducing the task-list
    speaker.runAndWait()
    for task in tasks: # Speaking each task sequentially from a list
        speaker.say(task)
        speaker.runAndWait()

def get_principles_list(file):
    with open(file, "r") as principles:
        principles_list = principles.readlines()
    
    return principles_list

def say_principles(principles):
    speaker = pyttsx3.init()
    voices = speaker.getProperty("voices")
    speaker.setProperty("voice", voices[1].id)
    speaker.say("Never forget the following principles")
    for p in principles:
        speaker.say(p)
        speaker.runAndWait()


if __name__ == '__main__':
    tasks = get_tasks_from_calendar()
    say_tasks(tasks, name="Lucas")
    principles = get_principles_list(file="principles.txt")
    say_principles(principles)





    
import datetime
import os.path
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def authorize():

    scopes = ["https://www.googleapis.com/auth/tasks", "https://www.googleapis.com/auth/calendar"]

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def get_list(task_list):

    creds = authorize()

    try:

        service = build("tasks", "v1", credentials=creds)

        tasks = service.tasks().list(tasklist=task_list).execute()

        return [task["title"] for task in tasks["items"]]

    except HttpError as error:
        print("An error occurred: ", error)


def get_birthdays(calendar_name):

    creds = authorize()

    try:

        service = build("calendar", "v3", credentials=creds)

        date = dt.datetime.now().date()
        min_time = dt.datetime.combine(date, dt.time(0, 0, 1)).isoformat()+ "Z"
        max_time = dt.datetime.combine(date, dt.time(0, 0, 2)).isoformat() + "Z"

        birthdays = service.events().list(calendarId=calendar_name, timeMin=min_time, timeMax=max_time).execute()

        return [birthday["summary"] for birthday in birthdays["items"]]

    except HttpError as error:
        print("An error occurred: ", error)


def get_appointments(calendar="primary"):

    creds = authorize()

    try:

        service = build("calendar", "v3", credentials=creds)

        now = dt.datetime.utcnow().isoformat() + "Z"

        appointments = service.events().list(calendarId=calendar, timeMin=now, maxResults=5, orderBy="startTime", singleEvents=True).execute()

        for appointment in appointments["items"]:
            title = appointment["summary"]
            start = appointment["start"]["date"] if appointment["start"].get("date") else appointment["start"]["dateTime"]
            end = appointment["end"]["date"] if appointment["end"].get("date") else appointment["end"]["dateTime"]
            print(f"{start} - {end}: {title}")

        # return [birthday["summary"] for birthday in birthdays["items"]]

    except HttpError as error:
        print("An error occurred: ", error)


# print(get_list("UHhMeHVYX2dhaGZWdGJ2ag"))
# print(get_birthdays("422aed951e577227681ab482cbc171bb278be3e292971fe0e7bda901c32ce43f@group.calendar.google.com"))
get_appointments()
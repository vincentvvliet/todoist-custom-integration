import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def authenticate():
    """
    Authentication flow for Google Calendar API
    """

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds

def process_events(tasks: list) -> None:
    """
    Use Google Calendar API to process events by finding corresponding eventId's and consequently deleting those events.
    """
    creds = authenticate()

    try:
        service = build("calendar", "v3", credentials=creds)

        # Overview of items to find and delete
        print(tasks)

        # Call the Calendar API
        print("Retrieving ID's...")

        # Find event id's for each task
        ids = []
        for task in tasks:
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    singleEvents=True,
                    orderBy="startTime",
                    q=task,
                )
                .execute()
            )
            events = events_result.get("items", [])
            if not events:
                print("No upcoming events found.")
                # return

            # Prints the start and name of the next 10 events
            for event in events:
                print(event["summary"])
                ids.append(event["id"])

        if len(ids) == 0:
            print("No events found to be deleted")
            return

        print("Finalized ID retrieval, the following ID's were found.")
        print(ids)

        # Delete event for each stored id
        for id in ids:
            print("Currently deleting event with ID {}".format(id))

            # Delete event
            service.events().delete(calendarId='primary', eventId=id).execute()

        print("Successfully deleted events.")

    except HttpError as error:
        print(f"An error occurred: {error}")

import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Define the scope for Google Calendar API
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Path to your service account key file
load_dotenv()
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")


def authenticate():
    """
    Authentication flow using a Google service account for Google Calendar API.
    """
    # Authenticate using service account credentials
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
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


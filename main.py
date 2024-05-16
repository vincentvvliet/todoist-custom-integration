import os
import requests
from dotenv import load_dotenv

def authenticate_google_calendar():
    google_calendar_api_key = os.getenv("GOOGLE_CALENDAR_API_KEY")
    # Use the API key to authenticate with Google Calendar API

def setup_todoist():
    # Use the API key to authenticate with Todoist API
    todoist_api_key = os.getenv("TODOIST_API_KEY")
    sync_token = '*'
    resource_types = '["items"]'

    # Prepare the headers with the bearer token
    headers = {
        "Authorization": f"Bearer {todoist_api_key}"
    }

    # Prepare the data for the request
    data = {
        "sync_token": sync_token,
        "resource_types": resource_types
    }

    return headers, data

def get_completed_tasks(headers, data):
    base_url = os.getenv("TODOIST_BASE_URL")

    # Make the request to the Todoist API
    response = requests.post(f"{base_url}/sync/v9/completed/get_all", headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Todoist API returned a successful response
        print("Todoist API authentication successful")
    else:
        # Todoist API returned an error response
        print(f"Todoist API authentication failed with status code {response.status_code}")
        print(response.text)  # Print the error response
        return None

    # Parse the JSON response
    response_data = response.json()

    # Access the relevant data from the response
    items = response_data.get('items', [])

    return items

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Setup Todoist headers and data
    headers, data = setup_todoist()

    # Retrieve completed tasks from Todoist
    completed_tasks = get_completed_tasks(headers, data)

    # Filter for only google calendar tasks
    completed_google_calendar_tasks = [task for task in completed_tasks if '@GCal' in task.get('content', '')]

    # Print completed tasks related to Google Calendar
    print("\nCompleted tasks related to Google Calendar:")
    for task in completed_google_calendar_tasks:
        print(task)
        # print(task.get('content', ''))

    # TODO: Retrieve event from Google Calendar corresponding to the task
    # TODO: Add event back to Google Calendar

if __name__ == '__main__':
    main()

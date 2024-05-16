import os
import requests

from dotenv import load_dotenv

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

def find_event_ids(tasks):
    base_url = os.getenv('GOOGLE_CALENDAR_BASE_URL')
    ids = []
    for task in tasks:
        print(task)
        response = requests.post(f"{base_url}calendars/calendarId/events")
        ids.append()

    return ids

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Setup Todoist headers and data
    headers, data = setup_todoist()

    # Retrieve completed tasks from Todoist
    completed_tasks = get_completed_tasks(headers, data)

    # Filter for only non google calendar tasks
    completed_todoist_tasks = [task.get('content', '') for task in completed_tasks if not '@GCal' in task.get('content', '')]

    # Find event ID's
    ids = find_event_ids(completed_todoist_tasks)

    # print("\nCompleted tasks originating from Todoist:")
    # for task in completed_todoist_tasks:
    #     print(task)
    #     response = requests.post(f"{google_calendar_base_url}calendars/calendarId/events", headers=headers, data=data)


    # TODO: Retrieve event from Google Calendar corresponding to the task
    # TODO: Remove event from Google Calendar (Events:delete)

if __name__ == '__main__':
    main()

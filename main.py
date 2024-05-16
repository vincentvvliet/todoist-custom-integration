import os
import requests
from quickstart import process_events
from dotenv import load_dotenv

KNOWN_BUGS = ['FP - week7A @FP', 'FP - week7B @FP']


def setup_todoist():
    # Use the API key to authenticate with Todoist API
    todoist_api_key = os.getenv("TODOIST_API_KEY")

    # Prepare the headers with the bearer token
    headers = {
        "Authorization": f"Bearer {todoist_api_key}"
    }

    # Prepare the data for the request
    data = {
        "sync_token": '*',
        "resource_types": '["items"]',
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
        print(response.text)
        return None

    # Parse the JSON response
    response_data = response.json()

    # Access the relevant data from the response
    return response_data.get('items', [])

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Setup Todoist headers and data
    headers, data = setup_todoist()

    # Retrieve completed tasks from Todoist
    completed_tasks = get_completed_tasks(headers, data)

    # Filter for only non google calendar tasks
    completed_todoist_tasks = [task.get('content', '') for task in completed_tasks if not '@GCal' in task.get('content', '')]

    # Filter out known problems from Todoist side
    completed_todoist_tasks = [task for task in completed_todoist_tasks if task not in KNOWN_BUGS]

    # Process events
    if len(completed_todoist_tasks) > 0:
        process_events(completed_todoist_tasks)
    else:
        print("No completed Todoist tasks to process")

if __name__ == '__main__':
    main()

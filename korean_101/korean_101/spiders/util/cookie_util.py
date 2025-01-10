import json
import os


def create_cookies_file_if_not_exists(file_name='cookies.json'):
    # Check if the file exists
    if not os.path.exists(file_name):
        # Create an empty JSON file
        with open(file_name, 'w') as file:
            json.dump([], file)


def get_cookies(file_name='cookies.json'):
    # Ensure the cookies file exists
    create_cookies_file_if_not_exists(file_name)

    with open(file_name, 'r') as file:
        cookies_list = json.load(file)

    # Convert cookie list to dictionary
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies_list}
# scrapy_cookies = {cookie["name"]: cookie["value"] for cookie in cookies}


    return cookies_dict

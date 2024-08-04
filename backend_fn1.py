import os
import json


def check_user_exists(username):
    if not os.path.exists('users.json'):
        # Create the file if it doesn't exist
        with open('users.json', 'w', encoding='utf-8') as f:
            json.dump({}, f)

    with open('users.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
        return username in users

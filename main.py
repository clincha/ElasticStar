import os

import requests
from dotenv import load_dotenv


def get_accounts():
    parameters = {
        'Authorization': 'Bearer ' + os.getenv('PERSONAL_ACCESS_TOKEN'),
    }

    response = requests.get("https://api.starlingbank.com/api/v2/accounts", headers=parameters)

    print(response.json())


if __name__ == '__main__':
    load_dotenv()
    get_accounts()

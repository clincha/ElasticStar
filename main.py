import os

import requests
from dotenv import load_dotenv


def get_accounts(personal_access_token):
    """
    Retuens all the starling Accounts associated with the Personal Access Token
    :param personal_access_token: Users Personal Access token
    :return: An array containing all the users accounts. Account object keys:
        - accountUid
        - accountType
        - defaultCategory
        - currency
        - createdAt
        - name
    """
    parameters = {
        'Authorization': 'Bearer ' + personal_access_token,
    }
    response = requests.get("https://api.starlingbank.com/api/v2/accounts", headers=parameters)
    return response.json()['accounts']


if __name__ == '__main__':
    load_dotenv()
    print(get_accounts(os.getenv('PERSONAL_ACCESS_TOKEN'))[0])

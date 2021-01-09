import os

import requests
from dotenv import load_dotenv


def get_accounts(personal_access_token):
    """
    Get an account holder's bank accounts
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


def get_statement_periods(personal_access_token, account_uid):
    """
    Get list of statement periods which are available for an account
    :param personal_access_token: Users Personal Access token
    :param account_uid: The accounts unique identifier
    :return: An array containing the statement periods. Statement period object keys:
        - period
        - partial
    """
    parameters = {
        'Authorization': 'Bearer ' + personal_access_token,
    }
    response = requests.get(
        "https://api.starlingbank.com/api/v2/accounts/" + account_uid + "/statement/available-periods",
        headers=parameters)
    return response.json()['periods']


if __name__ == '__main__':
    load_dotenv()
    pat = os.getenv('PERSONAL_ACCESS_TOKEN')

    accounts = get_accounts(pat)
    for account in accounts:
        statement_periods = get_statement_periods(pat, account['accountUid'])
        print(statement_periods)

import os
from csv import reader

import requests
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from datetime import datetime
import tqdm

base_url = "https://api.starlingbank.com/api/v2/"
timestamp_format = "%Y-%m-%dT%H:%M:%SZ"
elastic_index = "starling"


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
    headers = {
        'Authorization': "Bearer " + personal_access_token
    }
    response = requests.get("https://api.starlingbank.com/api/v2/accounts", headers=headers)
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
    headers = {
        'Authorization': "Bearer " + personal_access_token
    }
    response = requests.get(
        "https://api.starlingbank.com/api/v2/accounts/" + account_uid + "/statement/available-periods",
        headers=headers)
    return response.json()['periods']


def get_statement(personal_access_token, account_uid, period):
    """
    Download a statement for a given statement period
    :param personal_access_token: Users Personal Access token
    :param account_uid: The accounts unique identifier
    :param period: The year month string for the statement
    :return: A csv string with the headers:
        - Date
        - Counter Party
        - Reference
        - Type
        - Amount (GBP)
        - Balance (GBP)
        - Spending Category
    """
    headers = {
        'Authorization': "Bearer " + personal_access_token,
        'Accept': "text/csv"
    }
    params = {
        'yearMonth': period
    }
    response = requests.get(
        "https://api.starlingbank.com/api/v2/accounts/" + account_uid + "/statement/download",
        headers=headers,
        params=params)
    return response.text


def get_full_transaction_history(personal_access_token):
    """
    Gets the entire transaction history for all accounts associated with the personal access token provided
    :param personal_access_token: The Starling Personal Access Token
    :return: A list of transaction lines, which are in turn a list of strings
    """
    accounts = get_accounts(personal_access_token)
    statement_lines = []
    for account in accounts:
        statement_periods = get_statement_periods(personal_access_token, account['accountUid'])
        for statement_period in statement_periods:
            statement = get_statement(personal_access_token, account['accountUid'], statement_period['period'])
            statement = statement.split("\n")
            if statement_lines:
                statement = statement[1:]  # Remove heading row if this isn't the first statement
            for line in reader(statement):
                statement_lines.append(line)
    return list(filter(None, statement_lines))  # Remove the blank lines


def get_saving_spaces_for_account(personal_access_token):
    """
    Gets all the saving spaces associated with the given personal access token
    :param personal_access_token: The personal access token for the Starling account
    :return: A list of saving spaces which in turn are a list of strings
    """
    headers = {
        'Authorization': "Bearer " + personal_access_token
    }
    accounts = get_accounts(personal_access_token)
    all_goals = [['Account Name',
                  'Space Name',
                  'Target Amount',
                  'Saved Amount',
                  'Saved Percentage']]
    for account in accounts:
        response = requests.get(
            "https://api.starlingbank.com/api/v2/account/" + account['accountUid'] + "/savings-goals",
            headers=headers)
        for goal in response.json()['savingsGoalList']:
            accountName = account['name']
            goalName = goal['name']
            totalSaved = '£{0}'.format(goal['totalSaved']['minorUnits'] / 100)

            target = 'N/A'
            totalSavedPercentage = 'N/A'
            if 'target' in goal:
                target = '£{0}'.format(goal['target']['minorUnits'] / 100)
                if 'savedPercentage' in goal:
                    totalSavedPercentage = '{0}%'.format(goal['savedPercentage'])

            all_goals.append([accountName, goalName, target, totalSaved, totalSavedPercentage])
    return all_goals


def get_transaction_feed(personal_access_token, account_id):
    headers = {
        'Authorization': "Bearer " + personal_access_token
    }
    response = requests.get(base_url + "feed/account/" + account_id + "/settled-transactions-between?" +
                            "minTransactionTimestamp=" + "1000-01-01T00:00:00Z" +
                            "&"
                            "maxTransactionTimestamp=" + datetime.utcnow().strftime(timestamp_format),
                            headers=headers
                            )
    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)
        print(response.reason)
        print(response.url)
        exit(1)


def generate_actions(personal_access_token, account_id):
    for feedItem in get_transaction_feed(personal_access_token, account_id)['feedItems']:
        document = {
            "_id": feedItem['feedItemUid']
        }
        feedItem.pop('feedItemUid')
        document.update(feedItem)
        yield document


if __name__ == '__main__':
    print("Loading variables...")
    load_dotenv()
    print("Success!")
    print("Getting transaction history...")
    transactions = get_transaction_feed(os.getenv('PERSONAL_ACCESS_TOKEN'),
                                        get_accounts(os.getenv('PERSONAL_ACCESS_TOKEN'))[0]['accountUid'])
    print("Success!")
    print("Adding transactions to Elastic...")
    elastic = Elasticsearch(
        cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
        basic_auth=("elastic", os.getenv("ELASTIC_CLOUD_PASSWORD")))

    progress = tqdm.tqdm(unit="documents", total=sum(1 for _ in transactions['feedItems']))
    for ok, action in streaming_bulk(
            client=elastic,
            index=elastic_index,
            actions=generate_actions(os.getenv('PERSONAL_ACCESS_TOKEN'),
                                     get_accounts(os.getenv('PERSONAL_ACCESS_TOKEN'))[0]['accountUid'])
    ):
        progress.update(1)

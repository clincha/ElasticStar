import os
from csv import reader

import gspread
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


def clear_and_fill_sheet(workbook_id, sheet_name, data):
    gc = gspread.service_account("service_account.json")
    workbook = gc.open_by_key(workbook_id)
    sheet = workbook.worksheet(sheet_name)
    sheet.clear()
    sheet.append_rows(data, 'USER_ENTERED')


if __name__ == '__main__':
    load_dotenv()

    transaction_history = get_full_transaction_history(os.getenv('PERSONAL_ACCESS_TOKEN'))

    clear_and_fill_sheet(os.getenv('WORKBOOK_ID'), os.getenv('SHEET_NAME'), transaction_history)

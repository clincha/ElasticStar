import os

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


if __name__ == '__main__':
    load_dotenv()
    pat = os.getenv('PERSONAL_ACCESS_TOKEN')
    workbook_id = os.getenv('WORKBOOK_ID')
    sheet_name = os.getenv('SHEET_NAME')

    gc = gspread.service_account("service_account.json")
    workbook = gc.open_by_key(workbook_id)
    sheet = workbook.worksheet(sheet_name)
    sheet.clear()

    accounts = get_accounts(pat)
    for account in accounts:
        statement_periods = get_statement_periods(pat, account['accountUid'])
        statement_lines = [get_statement(pat,
                                         account['accountUid'],
                                         statement_periods[0]['period']).split("\n")[0].split(",")]  # Heading row
        for statement_period in statement_periods:
            statement = get_statement(pat, account['accountUid'], statement_period['period'])
            statement = statement.split("\n")
            statement = statement[1:]  # Remove heading row
            for row in statement:
                statement_lines.append(row.split(","))
        statement_lines = list(filter(lambda item: item != [''], statement_lines))  # Remove the blank lines
        sheet.append_rows(statement_lines, 'USER_ENTERED')

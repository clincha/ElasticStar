import os

import gspread
import variables
from starling import Starling


def update_transaction_sheet(account, transactions, workbook):
    print(f"Accessing sheet for {account.lower()} account...")
    try:
        worksheet = workbook.worksheet(f"starling-{account.lower()}")
    except gspread.exceptions.WorksheetNotFound:
        worksheet = workbook.add_worksheet(f"starling-{account.lower()}", 0, 0)

    print(f"Formatting transaction data...")
    data = [[
        "Currency",
        "Amount",
        "Source Currency",
        "Source Amount",
        "Direction",
        "Transaction Time",
        "Source",
        "Status",
        "Counter Party Type",
        "Counter Party Name",
        "Reference",
        "Country",
        "Spending Category",
        "Has Attachment",
        "Has Receipt"
    ]]
    for transaction in transactions:
        try:
            data.append([
                transaction.get('amount', "").get('currency', ""),
                transaction.get('amount', "").get('minorUnits', ""),
                transaction.get('sourceAmount', "").get('currency', ""),
                transaction.get('sourceAmount', "").get('minorUnits', ""),
                transaction.get('direction', ""),
                transaction.get('transactionTime', ""),
                transaction.get('source', ""),
                transaction.get('status', ""),
                transaction.get('counterPartyType', ""),
                transaction.get('counterPartyName', ""),
                transaction.get('reference', ""),
                transaction.get('country', ""),
                transaction.get('spendingCategory', ""),
                transaction.get('hasAttachment', ""),
                transaction.get('hasReceipt', ""),
            ])
        except KeyError as missing_key:
            # Instead of failing here we can just set the values to "" if they don't have data in the API
            print(f"Missing key for {missing_key}. Fatal transaction {transaction}")

    print(f"Adding transactions to sheet...")
    worksheet.update(range_name='A1',
                     values=data)


def update_saving_spaces_sheet(account, spaces, workbook):
    print(f"Accessing saving spaces sheet for {account.lower()} account...")
    try:
        worksheet = workbook.worksheet(f"starling-spaces-{account.lower()}")
    except gspread.exceptions.WorksheetNotFound:
        worksheet = workbook.add_worksheet(f"starling-spaces-{account.lower()}", 0, 0)

    print(f"Formatting saving spaces data...")
    data = [[
        "Space",
        "Target Currency",
        "Target",
        "Total Saved Currency",
        "Total Saved",
        "Saved Percentage",
        "State"
    ]]
    for space in spaces['savingsGoalList']:
        data.append(
            [
                space.get('name', ""),
                space.get('target', "").get('currency', ""),
                space.get('target', "").get('minorUnits', ""),
                space.get('totalSaved', "").get('currency', ""),
                space.get('totalSaved', "").get('minorUnits', ""),
                space.get('savedPercentage', ""),
                space.get('state', "")
            ]
        )
    print(f"Adding saving space data to sheet...")
    worksheet.update(range_name='A1',
                     values=data)


if __name__ == '__main__':
    print(f"Connecting to Google Sheets...")
    finance_workbook = gspread.service_account(filename="service_account.json").open("Finance")

    for starling_account in variables.accounts:
        print(f"Checking for {starling_account.lower()} access token...")
        access_token = f'{starling_account}_ACCESS_TOKEN'
        if access_token not in os.environ:
            print("Not found, skipping...")
            continue

        print(f"Getting data from {starling_account.lower()} account...")
        starling = Starling(
            os.getenv(access_token),
            sandbox=False)
        main_account = starling.get_accounts()[0]['accountUid']
        account_transactions = starling.get_transaction_feed(main_account)
        account_spaces = starling.get_saving_spaces(main_account)

        # update_transaction_sheet(starling_account, account_transactions, finance_workbook)
        update_saving_spaces_sheet(starling_account, account_spaces, finance_workbook)

        print(f"Successfully finished updating {starling_account.lower()} account!")

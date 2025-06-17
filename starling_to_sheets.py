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
        data.append([
            transaction.get('amount', "").get('currency', ""),
            transaction.get('amount', "").get('minorUnits', 0) / 100,
            transaction.get('sourceAmount', "").get('currency', ""),
            transaction.get('sourceAmount', "").get('minorUnits', 0) / 100,
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

    print(f"Adding transactions to sheet...")
    worksheet.clear()
    worksheet.freeze(rows=1)
    worksheet.update(range_name='A1',
                     values=data)
    worksheet.format(ranges="1:1", format={
        "textFormat": {
            "bold": True
        },
        "horizontalAlignment": "CENTER",
    })
    worksheet.format(ranges="B:B", format={
        "numberFormat": {
            "type": "CURRENCY",
        }
    })


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
        space_data = [
            space.get('name', "")
        ]

        if space.get('target'):
            space_data.append(space.get('target', "").get('currency', ""))
            space_data.append(space.get('target', "").get('minorUnits', 0) / 100)
        else:
            space_data.append("")
            space_data.append("")

        data.append(space_data + [
            space.get('totalSaved', "").get('currency', ""),
            space.get('totalSaved', "").get('minorUnits', 0) / 100,
            space.get('savedPercentage', 0) / 100,
            space.get('state', "")
        ])

    print(f"Adding saving space data to sheet...")
    worksheet.clear()
    worksheet.freeze(rows=1)
    worksheet.update(range_name='A1',
                     values=data)
    worksheet.format(ranges="1:1", format={
        "textFormat": {
            "bold": True
        },
        "horizontalAlignment": "CENTER",
    })
    worksheet.format(ranges=["C:C", "E:E"], format={
        "numberFormat": {
            "type": "CURRENCY",
        }
    })
    worksheet.format(ranges="F:F", format={
        "numberFormat": {
            "type": "PERCENT",
        }
    })


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

        update_transaction_sheet(starling_account, account_transactions, finance_workbook)
        update_saving_spaces_sheet(starling_account, account_spaces, finance_workbook)

        print(f"Successfully finished updating {starling_account.lower()} account!")

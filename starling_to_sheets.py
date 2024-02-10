import os

import gspread
import variables
from dotenv import load_dotenv
from starling import Starling

if __name__ == '__main__':
    for account in variables.accounts:
        access_token = f'{account}_ACCESS_TOKEN'
        if access_token not in os.environ:
            # Skip to the next account type
            continue

        print(f"Accessing sheet for {account.lower()} account...")
        google_account = gspread.service_account(filename="service_account.json")
        worksheet = google_account.open("Finance").worksheet(f"starling-{account.lower()}")

        print(f"Getting transaction history for {account.lower()} account...")
        starling = Starling(
            os.getenv(access_token),
            sandbox=False)
        main_account = starling.get_accounts()[0]['accountUid']
        transactions = starling.get_transaction_feed(main_account)

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
        for index, transaction in enumerate(transactions):
            try:
                data.append([
                    transaction['amount']['currency'],
                    transaction['amount']['minorUnits'],
                    transaction['sourceAmount']['currency'],
                    transaction['sourceAmount']['minorUnits'],
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

        print("Done!")

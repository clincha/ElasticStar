import os
from dotenv import load_dotenv
from trading212 import client
import gspread

load_dotenv()
accounts = ['ISA', 'INVEST']
finance_workbook = gspread.service_account(filename="service_account.json").open("Finance")

for account in accounts:
    api_key = os.getenv(f"TRADING212_{account}_API_KEY")
    t212 = client.Client(api_key)

    # Get account cash
    try:
        worksheet = finance_workbook.worksheet(f"trading212-{account.lower()}")
    except gspread.exceptions.WorksheetNotFound:
        worksheet = finance_workbook.add_worksheet(f"trading212-{account.lower()}", 0, 0)
    worksheet.update(range_name="A1", values=[[key.title(), value] for key, value in t212.get_account_cash().items()])
    worksheet.format("A:A", {
        "textFormat": {
            "bold": True
        },
        "horizontalAlignment": "CENTER",
    })
    worksheet.format("B:B", {
        "numberFormat": {"type": "CURRENCY"}
    })

    # Get account positions
    try:
        worksheet = finance_workbook.worksheet(f"trading212-{account.lower()}-positions")
    except gspread.exceptions.WorksheetNotFound:
        worksheet = finance_workbook.add_worksheet(f"trading212-{account.lower()}-positions", 0, 0)

    # Set headings
    data = [[
        'Ticker',
        'Quantity',
        'Currency',
        'Average Buy Price',
        'Current Price',
        'Predicted Profit/Loss',
        'Total Predicted P/L',
    ]]

    all_instruments = t212.get_instruments()
    for index, position in enumerate(t212.get_open_positions()):
        row = [
            position['ticker'],
            position['quantity'],
            next(inst['currencyCode'] for inst in all_instruments if inst['ticker'] == position['ticker']),
            position['averagePrice'],
            position['currentPrice'],
            position['ppl'],
            # Calculate the Total Predicted P/L
            f'='
            f'('
            f'  SWITCH('
            f'          C{index + 2},'  # We need to add 2 because the first row is the header and the index are 0-based
            f'          "GBP", 1,'
            f'          "GBX", 0.01,'
            f'          GOOGLEFINANCE(CONCATENATE("Currency:"&C{index + 2}&"GBP"))'
            f'      ) '  # Get the conversion rate to GBP
            f'  * E{index + 2}'  # Current Price in local currency
            f')'
            f' * B{index + 2}'  # Quantity
        ]
        data.append(row)

    worksheet.clear()
    worksheet.freeze(rows=1)
    worksheet.update(range_name="A1", values=data, raw=False)
    worksheet.format(ranges="1:1", format={
        "textFormat": {
            "bold": True
        },
        "horizontalAlignment": "CENTER",
    })
    worksheet.format(ranges="G:G", format={
        "numberFormat": {
            "type": "CURRENCY",
        }
    })

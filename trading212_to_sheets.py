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
    response = t212.get_account_cash()

    try:
        worksheet = finance_workbook.worksheet(f"trading212-{account.lower()}")
    except gspread.exceptions.WorksheetNotFound:
        worksheet = finance_workbook.add_worksheet(f"trading212-{account.lower()}", 0, 0)

    data = []
    for key, value in response.items():
        data.append([key, value])
    worksheet.update(range_name="A1", values=data)

for account in accounts:
    api_key = os.getenv(f"TRADING212_{account}_API_KEY")
    t212 = client.Client(api_key)
    positions = t212.get_open_positions()

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
        'Foreign Exchange Predicted P/L',
        'Total Predicted P/L',
    ]]

    all_instruments = t212.get_instruments()
    row_index = 1
    for position in positions:
        # Get the instrument details for the ticker
        instrument = next((inst for inst in all_instruments if inst['ticker'] == position['ticker']), None)
        row_index = row_index + 1
        row = [
            position['ticker'],
            position['quantity'],
            instrument['currencyCode'],
            position['averagePrice'],
            position['currentPrice'],
            position['ppl'],
            position['fxPpl'],
            # Calculate the Total Predicted P/L
            f'='
            f'SWITCH(C{row_index}, "GBP", 1, "GBX", 0.01, GOOGLEFINANCE(CONCATENATE("Currency:"&C{row_index}&"GBP")))'
            f' * E{row_index}'
            f' * D{row_index}'
        ]
        data.append(row)
    worksheet.update(range_name="A1", values=data, raw=False)

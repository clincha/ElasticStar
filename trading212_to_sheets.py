import os
from dotenv import load_dotenv
from trading212 import client
import gspread

load_dotenv()
accounts = ['ISA', 'INVEST']
finance_workbook = gspread.service_account(filename="service_account.json").open("Finance")

for account in accounts:
    api_key = os.getenv(f"TRADING212_{account}_API_KEY")
    t212 = client.Client(api_key, demo=True)
    response = t212.get_account_cash()

    try:
        worksheet = finance_workbook.worksheet(f"trading212-{account.lower()}")
    except gspread.exceptions.WorksheetNotFound:
        worksheet = finance_workbook.add_worksheet(f"trading212-{account.lower()}", 0, 0)

    data = []
    for key, value in response.items():
        data.append([key, value])
    worksheet.update(range_name="A1", values=data)

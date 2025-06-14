import os
from dotenv import load_dotenv
from trading212 import client
import gspread

load_dotenv()
t212 = client.Client(os.getenv("TRADING212_DEMO_API_KEY"), demo=True)

response = t212.get_account_cash()

account = "demo"
finance_workbook = gspread.service_account(filename="service_account.json").open("Finance")

try:
    worksheet = finance_workbook.worksheet(f"trading212-{account.lower()}")
except gspread.exceptions.WorksheetNotFound:
    worksheet = finance_workbook.add_worksheet(f"trading212-{account.lower()}", 0, 0)

data = []
for key, value in response.items():
    data.append([key, value])

worksheet.update(range_name="A1", values=data)

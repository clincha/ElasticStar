# Google Sheets

I've created a workflow called `populate-spreadsheets` which will grab data from the Starling accounts and populate a Google Sheet with the data. The workflow is triggered by the `populate-spreadsheet.yml` file in the `.github/workflows` directory. The workflow uses the `starling_to_sheets.py` script to populate the Google Sheet. The script uses the `gspread` library to interact with the Google Sheets API. 


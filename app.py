from flask import Flask, jsonify
import gspread
from google.oauth2.service_account import Credentials
import traceback

app = Flask(__name__)

# Path to your JSON key file (Ensure this file exists)
SERVICE_ACCOUNT_FILE = ""

# Google Sheets & Drive API scopes (Fixes Permission Error)
SCOPES = [
   "",
   "",        
]

try:
    # Authenticate with Google Sheets using Service Account
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    print("✅ Google Sheets API authentication successful!")
except Exception as auth_error:
    print(f"❌ Authentication Failed: {auth_error}")

# Your Google Sheet Details
SPREADSHEET_ID = ""
SHEET_NAME = ""  

@app.route("/get-sheet-data", methods=["GET"])
def get_sheet_data():
    try:
        # Open Google Sheet and get worksheet
        sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
        data = sheet.get_all_records()

        # Debugging: Print Data in Terminal
        print(f"✅ Retrieved {len(data)} records from {SHEET_NAME}.")
        return jsonify(data)
    
    except Exception as e:
        # Capture the full traceback for debugging
        error_message = traceback.format_exc()
        print(f"❌ Error: {error_message}")
        return jsonify({"error": error_message}), 500


if __name__ == "__main__":
    app.run(debug=True)

import os
import requests
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Set up Google Sheets credentials using base64-encoded secret
print("🔐 Decoding credentials from environment variable...")
creds_base64 = os.environ.get("GOOGLE_CREDS_BASE64")

if not creds_base64:
    raise Exception("❌ Missing GOOGLE_CREDS_BASE64 secret in GitHub Actions!")

with open("credentials.json", "wb") as f:
    f.write(creds_base64.encode("utf-8"))
    f.flush()

# Authorize Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open the sheet
sheet = client.open_by_key(os.environ["GOOGLE_SHEET_ID"]).sheet1

# Get today's date
today_str = datetime.now().strftime("%Y-%m-%d")
print(f"📅 Today's date: {today_str}")

# Read all sheet rows
rows = sheet.get_all_records()
match_found = False

for row in rows:
    row_date = row.get("Date", "").strip()
    if row_date == today_str:
        match_found = True
        title = row.get("Title", "").strip()
        description = row.get("Description", "").strip()
        cover_url = row.get("Cover Image URL", "").strip()
        book_link = row.get("Book Link", "").strip()

        print(f"\n✅ Found matching row for {today_str}:")
        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"Cover URL: {cover_url}")
        print(f"Book Link: {book_link}")

        # Construct message
        caption = f"📘 <b>{title}</b>\n\n{description}\n\n👉 <a href=\"{book_link}\">Download Book</a>"

        # Send to Telegram
        telegram_token = os.environ["TELEGRAM_BOT_TOKEN"]
        telegram_channel_id = os.environ["TELEGRAM_CHANNEL_ID"]

        payload = {
            "chat_id": telegram_channel_id,
            "photo": cover_url,
            "caption": caption,
            "parse_mode": "HTML"
        }

        print("\n📤 Sending message to Telegram...")
        response = requests.post(
            f"https://api.telegram.org/bot{telegram_token}/sendPhoto",
            data=payload
        )

        print(f"📡 Telegram response: {response.status_code}")
        print(f"Response body: {response.text}")
        break

if not match_found:
    print(f"⚠️ No post found for today ({today_str}). Make sure your sheet is updated.")

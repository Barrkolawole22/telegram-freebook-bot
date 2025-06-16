import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import datetime
import os

# Secrets
BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHANNEL_ID = os.environ['TELEGRAM_CHANNEL_ID']

# Google Sheets Auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Free Book Posts").sheet1
data = sheet.get_all_records()
today = datetime.datetime.now().strftime('%Y-%m-%d')

for row in data:
    if row['Date'] == today:
        message = f"""
📘 *Title:* {row['Book Title']}
✍️ *Author:* {row['Author']}
📂 *Category:* {row['Category']}
🔗 *Download:* {row['Link']}
📝 *Why You Should Read:* {row['Why Read?']}
"""
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={
            'chat_id': CHANNEL_ID,
            'text': message,
            'parse_mode': 'Markdown'
        })
        break

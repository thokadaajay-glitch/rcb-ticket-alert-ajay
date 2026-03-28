import requests
from bs4 import BeautifulSoup
import time

URL = "https://royalchallengers.com/"
CHECK_INTERVAL = 10  # seconds

BOT_TOKEN = "8729313595:AAHdkKRqlVtR0rce1yfozCtRrItT_Ueqohg"
CHAT_ID = "8732492486"

def send_telegram():
    msg = "🔥 RCB Tickets LIVE! Hurry 👉 https://royalchallengers.com/"

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

def check_ticket():
    try:
        res = requests.get(URL, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        if "BUY TICKET" in soup.text.upper():
            print("🔥 LIVE!")
            send_telegram()
            return True
        else:
            print("❌ Not live")

    except Exception as e:
        print("Error:", e)

    return False

print("🚀 Started monitoring...")

while True:
    if check_ticket():
        break
    time.sleep(CHECK_INTERVAL)
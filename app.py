import requests
import time

# 🔗 CONFIG
BOT_TOKEN = "8729313595:AAHdkKRqlVtR0rce1yfozCtRrItT_Ueqohg"
CHAT_ID = "-5140885371"   # your group id
URL = "https://shop.royalchallengers.com/ticket"

CHECK_INTERVAL = 10
ALERT_COOLDOWN = 300  # seconds

last_alert_time = 0


# 📩 Send Telegram message
def send_telegram():
    try:
        msg = "🚨🚨 RCB TICKETS LIVE 🚨🚨\n\nBook NOW 👉 https://shop.royalchallengers.com/ticket"

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": msg
        }

        requests.post(url, data=payload, timeout=10)
        print("✅ Alert sent")

    except Exception as e:
        print("Telegram Error:", e)


# 🔥 Burst alerts (same as your logic)
def burst_alert():
    for _ in range(3):
        send_telegram()
        time.sleep(2)


# 🎯 Main checker
def check_ticket():
    global last_alert_time

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        print("🔍 Checking ticket page...")

        res = requests.get(URL, headers=headers, timeout=10)
        text = res.text.lower()

        # ❌ Not available cases
        if any(x in text for x in [
            "tickets not available",
            "await further announcements",
            "sold out"
        ]):
            print("❌ Tickets not live")
            return

        # ✅ REAL detection (strong signals only)
        if any(keyword in text for keyword in [
            "add to cart",
            "select quantity"
        ]):
            now = time.time()

            if last_alert_time == 0:
                print("🔥 TICKETS LIVE")
                burst_alert()
                last_alert_time = now

            elif now - last_alert_time > ALERT_COOLDOWN:
                print("🔔 Reminder alert")
                send_telegram()
                last_alert_time = now

        else:
            print("❌ Still not live")

    except Exception as e:
        print("Error:", e)


# 🔁 Runner loop
if __name__ == "__main__":
    print("🚀 Bot started...")

    while True:
        check_ticket()
        time.sleep(CHECK_INTERVAL)
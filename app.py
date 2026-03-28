import requests
import time

URL = "https://royalchallengers.com/"
CHECK_INTERVAL = 10  # seconds
ALERT_COOLDOWN = 300  # 5 minutes

BOT_TOKEN = "8729313595:AAHdkKRqlVtR0rce1yfozCtRrItT_Ueqohg"
CHAT_ID = "8732492486"

last_alert_time = 0


def send_telegram():
    msg = "🚨🚨 RCB TICKETS ALERT by Ajay bot Monitoring🚨🚨\n\nCheck NOW 👉 https://royalchallengers.com/"

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )


def burst_alert():
    print("🔥 Sending burst alerts...")
    for _ in range(3):
        send_telegram()
        time.sleep(2)


def check_ticket():
    global last_alert_time

    try:
        res = requests.get(URL, timeout=10)
        text = res.text.lower()

        # Ignore obvious false signals
        if "sold out" in text or "coming soon" in text:
            print("❌ Not available")
            return

        # Detect possible availability
        if "buy ticket" in text:
            now = time.time()

            # First time → burst alert
            if last_alert_time == 0:
                print("🔥 FIRST DETECTION")
                burst_alert()
                last_alert_time = now

            # After that → cooldown alerts
            elif now - last_alert_time > ALERT_COOLDOWN:
                print("🔔 Sending reminder alert")
                send_telegram()
                last_alert_time = now

            else:
                print("⏳ Cooldown active...")

        else:
            print("❌ Not live")

    except Exception as e:
        print("Error:", e)


print("🚀 Monitoring started...")

while True:
    check_ticket()
    time.sleep(CHECK_INTERVAL)
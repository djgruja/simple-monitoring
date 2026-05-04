SLACK_BOT_TOKEN = "xoxb-11046112893829-11048745309702-jG5iKI5cVAt9TeObYMcG2LGH"
SLACK_CHANNEL_ID = "C0B1EP1JCLE"
CHECK_INTERVAL_MINUTES = 5

def send_slack_alert(status_code):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": SLACK_CHANNEL_ID,
        "text": f"🚨 *URL Monitor Alert!* \nTarget: {TARGET_URL}\nResponse Code: {status_code}"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        if not result.get("ok"):
            print(f"Slack API error: {result.get('error')}")
        else:
            print("Slack alert sent!")
    except Exception as e:
        print(f"Failed to call Slack API: {e}")

def check_url():
    print(f"Checking {TARGET_URL}...")
    try:
        response = requests.get(TARGET_URL, timeout=10)
        if response.status_code != 200:
            send_slack_alert(response.status_code)
    except requests.exceptions.RequestException:
        send_slack_alert("Connection Failed")

# Schedule and run
schedule.every(CHECK_INTERVAL_MINUTES).minutes.do(check_url)

if __name__ == "__main__":
    check_url()
    while True:
        schedule.run_pending()
        time.sleep(1)

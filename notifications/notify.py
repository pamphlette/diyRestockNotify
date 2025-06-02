import os
import http.client, urllib

PUSHOVER_API_KEY = os.getenv("PUSHOVER_API")
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER")

conn = http.client.HTTPSConnection("api.pushover.net:443")

# send a simple notification with optional URL to 
def notification(message: str, url: str = None) -> None:
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": PUSHOVER_API_KEY,
        "user": PUSHOVER_USER_KEY,
        "title": "restock!",
        "message": message
    }), { "Content-type": "application/x-www-form-urlencoded" })
    print(f"Notification sent: {message}")
    conn.getresponse()

if __name__ == "__main__":
    print("This module handles notifications. " \
          "Import it or call `notification()` directly.")
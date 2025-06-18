import time
import requests
import re
def check_login_status(d):
    """
    Checks whether the user is logged in to the Grab app.
    Returns True if logged in, False otherwise.
    Raises exception if something goes wrong.
    """
    try:
        # First, wait briefly for the main screen or login prompt to load
        time.sleep(0.3) 

        # Look for login screen indicators
        login_keywords = ["login", "sign in", "log in"]
        for keyword in login_keywords:
            if d(textMatches=f"(?i)^{keyword}$").exists():
                print("❌ Not logged in. Please log in first.")
                return False

        # Look for home screen keywords as positive signal
        home_keywords = ["Food", "Transport", "Mart", "Car", "Bike"]
        for keyword in home_keywords:
            if d(textContains=keyword).exists(timeout=0.5):
                print("✅ User is logged in.")
                return True

        print("⚠️ Could not determine login status. Assuming not logged in.")
        return False

    except Exception as e:
        print(f"[Error] Failed to check login status: {e}")
        return False
    

def clear_unexpected_popups(d):
    """
    Try to close common popups (promos, permissions).
    """
    closers = [
        {"textMatches": "(?i)skip|later|no|no thanks|×|x|dismiss"},
        {"resourceId": "com.grab.taxibooking:id/btn_close"},
        {"description": "Close"},
    ]

    try:
        for _ in range(3):  # Multiple attempts in case of multiple layers
            for selector in closers:
                try:
                    el = d(**selector)
                    if el.exists(timeout=1):
                        el.click()
                        print(f"[Popup] Closed: {selector}")
                        time.sleep(0.3)
                except Exception as e:
                    print(f"[Warning] Error closing popup: {selector} → {e}")
    except Exception as e:
        print(f"[Error] Unexpected error in popup cleanup: {e}")

def accept_permissions(d):
    """
    Try to accept permissions.
    """
    yes_word = ["ok", "yes", "accept"]
    time.sleep(1)

    try:
        for _ in range(5):  # Multiple attempts in case of multiple layers
            if d(textContains="access").wait(timeout=1):
                    print("Found text with 'access'")
                    for selector in yes_word:
                        try:
                            el = d(textMatches=f"(?i)^{re.escape(selector)}$")
                            if el.exists:
                                print(f"Exact match found: {el.info.get('text')}")
                                el.click()
                                print(f"[Popup] Clicked (exact): {selector}")
                                time.sleep(0.3)
                                continue

                            # Fallback: partial match without clickable filter
                            el = d(textMatches=f"(?i).*{re.escape(selector)}.*", clickable=True)
                            if el.exists:
                                print(f"Partial match found: {el.info.get('text')}")
                                el.click()
                                print(f"[Popup] Clicked (partial): {selector}")
                                time.sleep(0.3)
                        except Exception as e:
                            print(f"[Warning] Error accepting permission: {selector} → {e}")
    except Exception as e:
        print(f"[Error] Unexpected error in popup cleanup: {e}")


def notify_n8n(chat_id, message):
    webhook_url = "https://n8n-dev2.heypico.ai/webhook-test/45bf8a05-f4f5-4daf-a864-c2feb5a3f095"  # Replace with your n8n Webhook URL

    payload = {
        "chat_id": chat_id,
        "message": str(message)
    }

    try:
        response = requests.post(webhook_url, json=payload)
        print(f"n8n Webhook response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Failed to notify n8n: {e}")

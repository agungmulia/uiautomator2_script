import time


def check_login_status(d):
    """
    Checks whether the user is logged in to the Grab app.
    Returns True if logged in, False otherwise.
    Raises exception if something goes wrong.
    """
    try:
        # First, wait briefly for the main screen or login prompt to load
        time.sleep(5) 

        # Look for login screen indicators
        login_keywords = ["login", "sign in", "log in", "masuk"]
        for keyword in login_keywords:
            if d(textMatches=f"(?i){keyword}").exists(timeout=3):
                print("❌ Not logged in. Please log in first.")
                return False

        # Look for home screen keywords as positive signal
        home_keywords = ["Food", "Transport", "Mart", "Car", "Bike"]
        for keyword in home_keywords:
            if d(textContains=keyword).exists(timeout=3):
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
                    if el.exists(timeout=2):
                        el.click()
                        print(f"[Popup] Closed: {selector}")
                        time.sleep(1)
                except Exception as e:
                    print(f"[Warning] Error closing popup: {selector} → {e}")
    except Exception as e:
        print(f"[Error] Unexpected error in popup cleanup: {e}")

def accept_permissions(d):
    """
    Try to accept permissions.
    """
    yes_word = ["ok", "yes", "accept"]


    try:
        for _ in range(5):  # Multiple attempts in case of multiple layers
            if d(textContains="access").wait(timeout=5.0):
                    print("Found text with 'access'")
                    for selector in yes_word:
                        try:
                            el = d(text=selector)
                            if el.exists(timeout=2):
                                el.click()
                                print(f"[Popup] Closed: {selector}")
                                time.sleep(1)
                        except Exception as e:
                            print(f"[Warning] Error accepting permission: {selector} → {e}")
    except Exception as e:
        print(f"[Error] Unexpected error in popup cleanup: {e}")
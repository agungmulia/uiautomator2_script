import time
import re
def check_login_status(d):
    """
    Checks whether the user is logged in to the Grab app.
    Returns True if logged in, False otherwise.
    Raises exception if something goes wrong.
    """
    try:
        print("=== DEBUG: Checking login status ===")
        # First, wait briefly for the main screen or login prompt to load
        time.sleep(2) 
        print("=== DEBUG: All clickable elements ===")
        for el in d.xpath("//*").all():
            text = el.attrib.get("text", "").strip()
            if text:
                print(f"[Node] Text: '{text}'  |  Class: {el.attrib.get('class')}")
        # Look for login screen indicators
        login_keywords = ["login", "sign in", "log in"]
        for keyword in login_keywords:
            if d(textMatches=f"(?i)^{keyword}$").exists():
                print("❌ Not logged in. Please log in first.")
                return False

        # Look for home screen keywords as positive signal
        home_keywords = ["search", "redeem", "adventure"]
        for el in d.xpath("//*").all():
                        try:
                            text = el.attrib.get("text", "").strip().lower()
                            if not text:
                                continue

                            for keyword in home_keywords:
                                if keyword in text:
                                    return True
                        except Exception as e:
                            print("⚠️ Could not determine login status. Assuming not logged in.")
                            return False

    except Exception as e:
        print(f"[Error] Failed to check login status: {e}")
        return False
    

def clear_unexpected_popups(d):
    """
    Try to close popus.
    """
    print("=== DEBUG: Checking popups ===")

    yes_word = ["ok", "yes", "accept", "allow", "turn on", "awesome"]

    try:
        print("=== DEBUG: All clickable elements ===")
        for el in d.xpath("//*").all():
            text = el.attrib.get("text", "").strip()
            if text:
                print(f"[Node] Text: '{text}'  |  Class: {el.attrib.get('class')}")
        for _ in range(3):  # Multiple attempts in case of multiple layers
            if d(textContains="welcome").wait(timeout=0.5):
                    print("Found text with 'welcome'")
                    for el in d.xpath("//*").all():
                        try:
                            text = el.attrib.get("text", "").strip().lower()
                            if not text:
                                continue

                            for keyword in yes_word:
                                if keyword in text:
                                    print(f"[Match] Trying to click: '{text}'")
                                    el.click()
                                    print(f"[Clicked] Matched: {text}")
                                    break  # stop after one match
                        except Exception as e:
                            print(f"[Error] While processing node: {e}")
                    print("=== DEBUG: All clickable elements ===")
                    for el in d.xpath("//*").all():
                        text = el.attrib.get("text", "").strip()
                        if text:
                            print(f"[Node] Text: '{text}'  |  Class: {el.attrib.get('class')}")
        print("=== DEBUG: Checking popups finished ===")
                    
    except Exception as e:
        print(f"[Error] Unexpected error in popup cleanup: {e}")

def accept_permissions(d):
    """
    Try to accept permissions.
    """
    print("=== DEBUG: Checking permissions ===")
    yes_word = ["ok", "yes", "accept", "allow", "turn on", "awesome"]
    time.sleep(2)

    try:
        
        for _ in range(5):  # Multiple attempts in case of multiple layers
            if d(textContains="access").wait(timeout=0.5) or d(textContains="welcome").wait(timeout=0.5):
                    print("Found text with 'access'")
                    for el in d.xpath("//*").all():
                        try:
                            text = el.attrib.get("text", "").strip().lower()
                            if not text:
                                continue

                            for keyword in yes_word:
                                if keyword in text:
                                    print(f"[Match] Trying to click: '{text}'")
                                    el.click()
                                    print(f"[Clicked] Matched: {text}")
                                    break  # stop after one match
                        except Exception as e:
                            print(f"[Error] While processing node: {e}")
                    print("=== DEBUG: All clickable elements ===")
                    for el in d.xpath("//*").all():
                        text = el.attrib.get("text", "").strip()
                        if text:
                            print(f"[Node] Text: '{text}'  |  Class: {el.attrib.get('class')}")
        print("=== DEBUG: Checking permissions finished ===")
    except Exception as e:
        print(f"[Error] Unexpected error in popup cleanup: {e}")

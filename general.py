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
            if d(textMatches=f"(?i)^{keyword}$").exists(timeout=0.3):
                print("❌ Not logged in. Please log in first.")
                return False

        # Look for home screen keywords as positive signal
        home_keywords = ["Food", "Transport", "Mart", "Car", "Bike"]
        for keyword in home_keywords:
            if d(textContains=keyword).exists(timeout=0.3):
                print("✅ User is logged in.")
                return True

        print("⚠️ Could not determine login status. Assuming not logged in.")
        return False

    except Exception as e:
        print(f"[Error] Failed to check login status: {e}")
        return False
    

def clear_unexpected_popups(d, resource_id = "com.grab.taxibooking:id/btn_close"):
    """
    Try to close common popups (promos, permissions).
    """
    closeKeyWord = ["skip", "no thanks", "dismiss"]


    while True:
        try:
            for selector in closeKeyWord:
                try:
                    el = d(textMatches=f"(?i)^{selector}$")
                    if el.exists(timeout=0.3):
                        print(selector)
                        print(el)
                        el.click()
                        print(f"[Popup] Closed: {selector}")
                        time.sleep(0.3)
                except Exception as e:
                    print(f"[Warning] Error closing popup: {selector} → {e}")
        except Exception as e:
            print(f"[Error] Unexpected error in popup cleanup: {e}")
        time.sleep(0.3)

def accept_permissions(d):
    """
    Try to accept permissions.
    """
    yes_word = ["ok", "yes", "accept", "allow", "turn on"]
    time.sleep(0.5)

    while True:
        try:
            if d(textMatches="(?i).*access|push notification.*").wait(timeout=0.4):
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
                        time.sleep(0.3)
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

def screen_components(d):
    xml = d.dump_hierarchy()  # Get UI XML
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml)
    elements = []
    for node in root.iter():
        if (not node.attrib.get("package", "").startswith("com.android")) and node.attrib.get("clickable") == "true":  # Only include Android widgets
            print(node.attrib)
        res_id = node.attrib.get("resource-id", "")
        text = node.attrib.get("text", "")
        if res_id or text:  # Only include elements with at least one property
            elements.append({
                "resource-id": res_id,
                "text": text,
                "class": node.attrib.get("class", ""),
                "bounds": node.attrib.get("bounds", ""),
                "clickable": node.attrib.get("clickable", "")
            })
    # Print all elements with both properties
    for elem in elements:
        if elem["resource-id"] and elem["text"]:
            print(f"ID: {elem['resource-id']} | Text: '{elem['text']}' | Class: {elem['class']} | Bounds: {elem['bounds']} | Clickable: {elem['clickable']}")

def find_components(d, text: str):
    xml = d.dump_hierarchy()  # Get UI XML
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml)
    for node in root.iter():
        if node.attrib.get("text") is not None and node.attrib.get("text").lower() == text:  # Only include Android widgets
            res_id = node.attrib.get("resource-id", "")
            text = node.attrib.get("text", "")
            return {
                "resource-id": res_id,
                "text": text,
                "class": node.attrib.get("class", ""),
                "bounds": node.attrib.get("bounds", ""),
                "clickable": node.attrib.get("clickable", "")
            }

def find_components_by_class_text(d, class_name: str, text: str):
    xml = d.dump_hierarchy()  # Get UI XML
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml)
    for node in root.iter():
        if node.attrib.get("text") is not None and node.attrib.get("class").lower() == class_name:
            print("comparing:", node.attrib.get("text").lower(), text, node.attrib.get("class").lower(), class_name)
            print(f"is it equal? {node.attrib.get('text').lower()} {text} {node.attrib.get('text').lower() == text}")
        if node.attrib.get("text") is not None and node.attrib.get("class").lower() == class_name and text in node.attrib.get("text").lower():  # Only include Android widgets
            res_id = node.attrib.get("resource-id", "")
            text = node.attrib.get("text", "")
            return {
                "resource-id": res_id,
                "text": text,
                "class": node.attrib.get("class", ""),
                "bounds": node.attrib.get("bounds", ""),
                "clickable": node.attrib.get("clickable", "")
            }
def find_components_by_id(d, id: str):
    xml = d.dump_hierarchy()  # Get UI XML
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml)
    comps = []
    for node in root.iter():
        if node.attrib.get("resource-id") == id:  # Only include Android widgets
            res_id = node.attrib.get("resource-id", "")
            text = node.attrib.get("text", "")
            comps.append({
                "resource-id": res_id,
                "text": text,
                "class": node.attrib.get("class", ""),
                "bounds": node.attrib.get("bounds", ""),
                "clickable": node.attrib.get("clickable", "")
            })
    return comps
def coordinate_bounds(bounds: str):
    x1, y1, x2, y2 = map(int, bounds.strip("[]").replace("][", ",").split(","))
    # Calculate center (x, y)
    center_x = (x1 + x2) // 2 
    center_y = (y1 + y2) // 2 
    return center_x, center_y
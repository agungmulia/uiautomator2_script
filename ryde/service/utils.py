import time
import re

def select_language(d):
    if d(text="Select Language").exists():
        d(text="English").click()

def check_login_status(d):
    """
    Checks whether the user is logged in to the Grab app.
    Returns True if logged in, False otherwise.
    Raises exception if something goes wrong.
    """
    try:
        print("=== DEBUG: Checking login status ===")
        # First, wait briefly for the main screen or login prompt to load
        # Look for login screen indicators
        for el in d.xpath("//*").all():
            text = el.attrib.get("text", "").strip()
            if text:
                print(f"[Node] Text: '{text}'  |  Class: {el.attrib.get('class')}")
        login_keywords = ["login", "sign in", "log in", "send code to sms"]

        for keyword in login_keywords:
            if d(textMatches=fr"(?i).*{keyword}.*").exists:
                print("❌ Not logged in. Please log in first.")
                return False
        return True
    except Exception as e:
        print(f"[Error] Failed to check login status: {e}")
        return False
    

def clear_unexpected_popups(d):
    """
    Try to close popus.
    """
    print("=== DEBUG: Checking popups ===")

    yes_word = ["ok", "yes", "turn on", "awesome", "skip", "no thanks", "dismiss"]

    try:
        if d(resourceId="com.rydesharing.ryde:id/imv_float_close").exists():
            close_comp = find_components_by_id(d, "com.rydesharing.ryde:id/imv_float_close")
            d.click(*coordinate_bounds(close_comp[0]["bounds"]))
        texts = []
        for el in d.xpath("//*").all():
            text = el.attrib.get("text", "").strip()
            texts.append(text.lower())
            if text:
                print(f"[Node] Text: '{text}'  |  Class: {el.attrib.get('class')}")
        print("texts:", texts)
        for _ in range(3):  # Multiple attempts in case of multiple layers
            
            if any(any(word in t.lower() for word in yes_word) for t in texts):
                    print("yang ini gan")
                    print("Found text with 'welcome'")
                    for el in d.xpath("//*").all():
                        try:
                            text = el.attrib.get("text", "").strip().lower()
                            if not text:
                                continue

                            for keyword in yes_word:
                                if keyword in text:
                                    if keyword == "ok" and text == "facebook":
                                        continue
                                    print(f"[Match] Trying to click: '{text}' {keyword}")
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

    try:
        
        for _ in range(4):  # Multiple attempts in case of multiple layers
            if d(textContains="access").wait(timeout=0.2):
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
        if node.attrib.get("text").lower() == text:  # Only include Android widgets
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
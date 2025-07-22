import uiautomator2 as u2
import time
from utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds

def check_incoming_message(users = None):
    try:
        d = u2.connect()
        d.app_start("com.whatsapp")

        while not d(resourceId="com.whatsapp:id/navigation_bar_item_large_label_view").exists():
            time.sleep(0.3)
        msg = []
        if d(resourceId="com.whatsapp:id/conversations_row_message_count").exists():
                        nodes = d.xpath('//*[@resource-id="com.whatsapp:id/conversations_row_message_count"]').all()

                        for node in nodes:
                            # Get the full path of the message count element
                            node_info = node.attrib
                            bounds = node_info.get('bounds')

                            if bounds:
                                # Use XPath from the root to get the contact name in the same row
                                # Go up 3 levels (bottom_row -> row_content), then find the contact name below
                                contact_xpath = f'//*[@bounds="{bounds}"]/../../..//*[@resource-id="com.whatsapp:id/conversations_row_contact_name"]'
                                contact_node = d.xpath(contact_xpath)

                                if contact_node.exists:
                                    contact_name = contact_node.get_text()
                                    print("Contact name:", contact_name)
                                    if contact_name in users:
                                        contact_node.click()
                                        while not d(resourceId="com.whatsapp:id/message_text").exists():
                                            time.sleep(0.3)
                                        ln = len(d(resourceId="com.whatsapp:id/message_text"))
                                        reply = d(resourceId="com.whatsapp:id/message_text")[ln-1].get_text()
                                        msg.append({"user": contact_name, "reply": reply})
                                        d.press("back")
                                        time.sleep(0.4)
                       
        print("msg", msg)
        return {"message": "check incoming message", "status": "success", "msg": msg}

    except Exception as e:
        print(f"[Error] Failed to check incoming message: {e}")
        import traceback
        print(traceback.format_exc())
        return {"message": "check incoming message", "status": "failed", "error": str(e)}
    
if __name__ == "__main__":
    check_incoming_message([])
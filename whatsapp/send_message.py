import uiautomator2 as u2
import time
import requests
import schedule
import threading
from PIL import Image
import io
from .utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
from .check_incoming import check_incoming_message
def send_message(tos= [], text = ""):
    d = u2.connect()
    d.app_start("com.whatsapp", stop=False)

    while not (d(resourceId="com.whatsapp:id/choose_language").exists() or d(resourceId="com.whatsapp:id/eula_accept").exists() or d(resourceId="com.whatsapp:id/search_bar_inner_layout").exists()):
        print("wait for comp")
        time.sleep(0.5)

    if not d(resourceId="com.whatsapp:id/search_bar_inner_layout").exists():
        res = login(d)
        return res
    
    to_options = []
    for to in tos:
        print("loop for: ", to)
        while not d(resourceId="com.whatsapp:id/search_bar_inner_layout").exists():
            time.sleep(0.3)
        d(resourceId="com.whatsapp:id/search_bar_inner_layout").click()

        while not d(resourceId="com.whatsapp:id/search_input").exists():
            time.sleep(0.2)
        d(resourceId="com.whatsapp:id/search_input").send_keys(to)

        # while not d(resourceId="com.whatsapp:id/contact_row_container")
        time.sleep(1.5)
        
        if len(d(resourceId="com.whatsapp:id/conversations_row_contact_name")) > 1:
            contact_list = []
            for v in d(resourceId="com.whatsapp:id/conversations_row_contact_name"):
                contact_list.append(v.get_text())
            to_options.append({"to": to, "options": contact_list})
            # return {"message": "contact list", "status": "choose_contact", "contact": contact_list}
        # elif len(d(resourceId="com.whatsapp:id/conversations_row_contact_name")) == 1:
        #     d(resourceId="com.whatsapp:id/conversations_row_contact_name").click()

        #     while not d(resourceId="com.whatsapp:id/entry").exists():
        #         time.sleep(0.2)
        #     d(resourceId="com.whatsapp:id/entry").send_keys(text)
        #     time.sleep(0.4)
        #     d(resourceId="com.whatsapp:id/send").click()

            # return {"message": "message sent", "status": "success"}
        d.press("back")
        d.press("back")
        #  check if any contact has options, if yes, return the options, if all tos have no options, just send the message
    if len(to_options) > 1:
        return {"message": "contact list", "status": "choose_contact", "contact": to_options}
    else:
        for to in tos:
            d(resourceId="com.whatsapp:id/search_bar_inner_layout").click()
            while not d(resourceId="com.whatsapp:id/search_input").exists():
                time.sleep(0.2)
            d(resourceId="com.whatsapp:id/search_input").send_keys(to)
            time.sleep(1.5)
            d(resourceId="com.whatsapp:id/conversations_row_contact_name").click()

            while not d(resourceId="com.whatsapp:id/entry").exists():
                time.sleep(0.2)
            d(resourceId="com.whatsapp:id/entry").send_keys(text)
            time.sleep(0.4)
            d(resourceId="com.whatsapp:id/send").click()
            d.press("back")
        # set check
        # check_for_reply(tos)
        res = {"message": "message sent", "status": "success"}
        print(res)
        # send http req
        return res

        
        
    
def login(d):
    while not (d(resourceId="com.whatsapp:id/choose_language").exists() or d(resourceId="com.whatsapp:id/eula_accept").exists()):
        time.sleep(0.2)
    time.sleep(1)
    if d(resourceId="com.whatsapp:id/choose_language").exists():
        d(resourceId="com.whatsapp:id/next_button").click()
    time.sleep(1)
    if d(resourceId="com.whatsapp:id/eula_accept").exists():
        d(resourceId="com.whatsapp:id/eula_accept").click()
    accept_permissions(d)

    while not d(resourceId="com.whatsapp:id/menuitem_overflow").exists():
        time.sleep(0.3)
    d(resourceId="com.whatsapp:id/menuitem_overflow").click()

    while not d(text="Link as companion device").exists():
        time.sleep(0.2)
    d(text="Link as companion device").click()
    time.sleep(2)
    d.screenshot("qr.jpeg")
    # Step 2: Open the PNG and convert to JPEG
    image = Image.open("qr.jpeg")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=60)  # Reduce quality for smaller size
    buffer.seek(0)
        # Step 3: Upload the image as a file
    url = 'https://api.heypico.ai/upload-file'
    files = {'file': ('qr.jpeg', buffer, 'image/jpeg')}

    response = requests.post(url, files=files)

    # Step 4: Print result
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)
    print("url:", response.json()["url"])
    if response.status_code != 201:
        return {"message":"get qr failed", "status": "failed"}
    return {"message":"get qr success", "status": "not_logged_in", "login_qr": response.json()["url"]}

def check_for_reply(tos, timeout_minutes=3):
    start_time = time.time()
    schedule.every(1).minutes.do(check_incoming_message, tos)

    def run_scheduler():
        while time.time() - start_time < timeout_minutes * 60:
            schedule.run_pending()
            time.sleep(1)
        print(f"Stopping worker for users {tos}")

    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()

if __name__ == "__main__":
    send_message(["kebskunka"], "hai")
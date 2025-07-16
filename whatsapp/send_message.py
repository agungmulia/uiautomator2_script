import uiautomator2 as u2
import time
import threading
import requests
from PIL import Image
import io
from .utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds

def send_message(to, text):
    d = u2.connect()
    d.app_start("com.whatsapp", stop=True)

    while not (d(resourceId="com.whatsapp:id/choose_language").exists() or d(resourceId="com.whatsapp:id/eula_accept").exists() or d(resourceId="com.whatsapp:id/search_bar_inner_layout").exists()):
        time.sleep(0.5)

    if not d(resourceId="com.whatsapp:id/search_bar_inner_layout").exists():
        res = login(d)
        return res
    
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
        
        return {"message": "contact list", "status": "choose_contact", "contact": contact_list}
    elif len(d(resourceId="com.whatsapp:id/conversations_row_contact_name")) == 1:
        d(resourceId="com.whatsapp:id/conversations_row_contact_name").click()

        while not d(resourceId="com.whatsapp:id/entry").exists():
            time.sleep(0.2)
        d(resourceId="com.whatsapp:id/entry").send_keys(text)
        time.sleep(0.4)
        d(resourceId="com.whatsapp:id/send").click()

        return {"message": "message sent", "status": "success"}
    
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
    time.sleep(1)

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
    if response.status_code != 200:
        return {"message":"get qr failed", "status": "failed"}
    return {"message":"get qr success", "status": "success", "qr": response.json()["url"]}

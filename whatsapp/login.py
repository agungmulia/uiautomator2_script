import uiautomator2 as u2
import time
import threading
from .utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
import base64
from PIL import Image
import io

def login():
    d = u2.connect()
    d.app_start("com.whatsapp", stop=False)

    # while not (d(resourceId="com.whatsapp:id/choose_language").exists() or d(resourceId="com.whatsapp:id/eula_accept").exists()):
    #     time.sleep(0.2)
    # if d(resourceId="com.whatsapp:id/choose_language").exists():
    #     d(resourceId="com.whatsapp:id/next_button").click()
    # if d(resourceId="com.whatsapp:id/eula_accept").exists():
    #     d(resourceId="com.whatsapp:id/eula_accept").click()
    # accept_permissions(d)


    d.screenshot("qr.jpeg")
    # Step 2: Open the PNG and convert to JPEG
    image = Image.open("qr.jpeg")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=60)  # Reduce quality for smaller size
    buffer.seek(0)

    # Step 3: Encode to base64
    encoded_string = base64.b64encode(buffer.read()).decode("utf-8")

    data_uri = f"data:image/jpeg;base64,{encoded_string}"

    return {"message":"get qr success", "status": "success", "qr": data_uri}

def login_otp(otp):
    d = u2.connect()
    d.app_start("com.whatsapp", stop=False)
    # while not d(resourceId="com.whatsapp:id/verify_sms_code_input").exists():
    #     time.sleep(0.2)
    # d(resourceId="com.whatsapp:id/verify_sms_code_input").send_keys(otp)

    # while not d(resourceId="com.whatsapp:id/permission_title").exists():
    #     time.sleep(0.2)
    # d(resourceId="com.whatsapp:id/submit").click()

    # accept_permissions(d)

    # print( {"message":"login success", "status": "success", "qr": encoded_string})
if __name__ == "__main__":
    # login("8565075699")
    login_otp("783780")
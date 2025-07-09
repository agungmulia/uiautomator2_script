import uiautomator2 as u2
import time
import threading
from .utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds

def login(phone_no):
    d = u2.connect()
    d.app_start("com.whatsapp", stop=False)

    if d(resourceId="com.whatsapp:id/choose_language").exists():
        d(resourceId="com.whatsapp:id/next_button").click()
    
    accept_permissions(d)

    # input phone number
    while not d(resourceId="com.whatsapp:id/registration_cc").exists():
        time.sleep(0.2)

    d(resourceId="com.whatsapp:id/registration_cc").send_keys("65")
    d(resourceId="com.whatsapp:id/registration_phone").send_keys(phone_no)
    d(resourceId="com.whatsapp:id/registration_submit").click()
    # time.sleep(1)
    # return

if __name__ == "__main__":
    login("6876786786")
import uiautomator2 as u2
import time
from .utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def login(phone_no):
    try:
        d = u2.connect()
        d.app_start("com.rydesharing.ryde", stop=False)
        # if phone_no starts with 0, remove it, but if starts with +xx, delete the +xx
        if phone_no.startswith("0"):
            phone_no = phone_no[1:]
        elif phone_no.startswith("+"):
            phone_no = phone_no[3:]
        elif phone_no.startswith("6"):
            phone_no = phone_no[2:]
        
        if d(resourceId="com.rydesharing.ryde:id/btn_login_mobile").exists():
            d(resourceId="com.rydesharing.ryde:id/btn_login_mobile").click()
        
        time.sleep(1)
        while not d(resourceId="com.rydesharing.ryde:id/et_phone").exists():
            time.sleep(0.2)
        d(resourceId="com.rydesharing.ryde:id/et_phone").send_keys(phone_no)

        while not d(resourceId="com.rydesharing.ryde:id/btn_get_otp").exists():
            time.sleep(0.2)
        d(resourceId="com.rydesharing.ryde:id/btn_get_otp").click()
        
        
        return {"message":"waiting otp", "status": "success"}
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return

def login_otp(otp):
    try:
        d = u2.connect()
        d.app_start("com.rydesharing.ryde", stop=False)
        if d(resourceId="com.rydesharing.ryde:id/et_pin_1").exists():
            otp_comp = d(resourceId="com.rydesharing.ryde:id/et_pin_1")
            otp_comp.click()
            for i in range(6):
                d.shell(f"input text '{otp[i]}'")
        # print("cek permission")
        # while not 
        return {"message":"login success", "status": "success"}
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
    
if __name__ == "__main__":
    # login("6580685170")
    login_otp("756508")
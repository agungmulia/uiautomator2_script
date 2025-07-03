import uiautomator2 as u2
import time
from .utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def login(phone_no):
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        d = u2.connect()
        if d.app_current()['package'] != "com.codigo.comfort":
            d.app_start("com.codigo.comfort", stop=False)
        # if phone_no starts with 0, remove it, but if starts with +xx, delete the +xx
        if phone_no.startswith("0"):
            phone_no = phone_no[1:]
        elif phone_no.startswith("+"):
            phone_no = phone_no[3:]
        elif phone_no.startswith("6"):
            phone_no = phone_no[2:]
        
        if d(resourceId="btnLogin").exists():
            d(resourceId="btnLogin").click()
        
        time.sleep(4)
        while not d(resourceId="txtMobileNumber").exists():
            time.sleep(0.2)
        d(resourceId="txtMobileNumber").send_keys(phone_no)

        while not d(resourceId="btnNext").exists():
            time.sleep(0.2)
        d(resourceId="btnNext").click()
        
        while not d(resourceId="txtOTPInput").exists():
            time.sleep(0.2)
        
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
        if d.app_current()['package'] != "com.codigo.comfort":
            d.app_start("com.codigo.comfort", stop=False)
        # # # if phone_no starts with 0, remove it, but if starts with +xx, delete the +xx
        if d(resourceId="txtOTPInput").exists():
            d(resourceId="txtOTPInput").send_keys(otp)
        print("cek permission")
        accept_permissions(d)
        print("cek popup")
        clear_unexpected_popups(d)
        return {"message":"login success", "status": "success"}
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
    
if __name__ == "__main__":
    login("6580685170")
    # login_otp("9101")
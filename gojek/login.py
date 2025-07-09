import uiautomator2 as u2
import time
from .utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def login(phone_no):
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        d.app_start("com.gojek.app", stop=False)
        # if phone_no starts with 0, remove it, but if starts with +xx, delete the +xx
        if phone_no.startswith("0"):
            phone_no = phone_no[1:]
        elif phone_no.startswith("+"):
            phone_no = phone_no[1:]
        while not d(resourceId="com.gojek.app:id/2131372066").exists():
            time.sleep(0.2)
        d(resourceId="com.gojek.app:id/2131372066").click()
        # text box com.gojek.app:id/2131369911
        d(resourceId="com.gojek.app:id/2131369911").send_keys(phone_no)
        # continute btn com.gojek.app:id/2131372066
        d(resourceId="com.gojek.app:id/2131372066").click()
        time.sleep(1.5)
        while not d(resourceId="com.gojek.app:id/2131372066")[1].exists():
            time.sleep(0.2)
            print("wait for btn")
        
        time.sleep(0.3)
        time.sleep(2)
        if find_components(d, "whatsapp") is not None:
            return {"message":"waiting whatsapp otp", "status": "success"}
        comp = d(resourceId="com.gojek.app:id/2131372066")[1]
        bounds_raw = comp.bounds()
        print("bounds_raw", bounds_raw)
        print("klik")
        bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
        d.click(*coordinate_bounds(bounds))     
        
        while not d(resourceId="com.gojek.app:id/2131369420").exists():
            time.sleep(0.2)
            print("wait for sms")
        comp = d(resourceId="com.gojek.app:id/2131369420")[0]
        bounds_raw = comp.bounds()
        print("klik")
        bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
        d.click(*coordinate_bounds(bounds))
        while not find_components(d, "sent via sms") is not None:
            if find_components(d, "fail") is not None:
                return {"status": "failed", "message": "otp not sent"}
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
        # sess = d.session("com.gojek.app") 
        d.app_start("com.gojek.app", stop=False)
        # if phone_no starts with 0, remove it, but if starts with +xx, delete the +xx
        if d(resourceId="com.gojek.app:id/2131374678").exists():
            d(resourceId="com.gojek.app:id/2131374678").send_keys(otp)
        
        accept_permissions(d)
        clear_unexpected_popups(d)
        time.sleep(1)
        if find_components(d, "indonesia") is not None and find_components(d, "singapore") is not None:
            sgp_btn = find_components(d, "singapore")
            d.click(*coordinate_bounds(sgp_btn["bounds"]))
            cfm_btn = find_components(d, "i'm in")
            d.click(*coordinate_bounds(cfm_btn["bounds"]))
        accept_permissions(d)
        clear_unexpected_popups(d)
        return {"message":"login success", "status": "success"}
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
    
if __name__ == "__main__":
    login("085249821174")
    # login_otp("3478")
import uiautomator2 as u2
import time
from general import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def login(phone_no):
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        d.app_start("com.grabtaxi.passenger", stop=False)
        # if phone_no starts with 0, remove it, but if starts with +xx, delete the +xx
        if phone_no.startswith("0"):
            phone_no = phone_no[1:]
        elif phone_no.startswith("+"):
            phone_no = phone_no[1:]
        
        if d(resourceId="com.grabtaxi.passenger:id/gds_button_content_layout")[1].exists():
            d(resourceId="com.grabtaxi.passenger:id/gds_button_content_layout")[1].click()
        
        time.sleep(1)
        while not d(resourceId="com.grabtaxi.passenger:id/btn_phone_number").exists():
            time.sleep(0.2)
        d(resourceId="com.grabtaxi.passenger:id/btn_phone_number").click()
        
        while not d(resourceId="com.grabtaxi.passenger:id/verify_number_edit_number").exists():
            time.sleep(0.2)
        d(resourceId="com.grabtaxi.passenger:id/verify_number_edit_number").send_keys(phone_no)
        
        while not d(resourceId="com.grabtaxi.passenger:id/btn_next_verify_number").exists():
            time.sleep(0.2)
        next_btn = d(resourceId="com.grabtaxi.passenger:id/btn_next_verify_number")
        bounds_raw = next_btn.bounds()
        bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
        d.click(*coordinate_bounds(bounds))
        
        while not d(resourceId="com.grabtaxi.passenger:id/verify_otp_edit_number").exists():
            return {"message":"waiting otp", "status": "success"}
        
        # return {"message":"waiting otp", "status": "success"}
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
        d.app_start("com.grabtaxi.passenger", stop=False)
        # if phone_no starts with 0, remove it, but if starts with +xx, delete the +xx
        if d(resourceId="com.grabtaxi.passenger:id/verify_otp_edit_number").exists():
            d(resourceId="com.grabtaxi.passenger:id/verify_otp_edit_number").send_keys(otp)
        
        time.sleep(2)
        if d(text="Transportation").exists():
            return {"message":"login success", "status": "success"}
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
    
if __name__ == "__main__":
    # login("085249821174")
    login_otp("356038")
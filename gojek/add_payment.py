import uiautomator2 as u2
import time
from .utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def add_payment(card_num, expiry, cvv):
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        d.app_start("com.gojek.app", stop=False)

        # press payment button
        while not d(resourceId="com.gojek.app:id/2131374409").exists():
            time.sleep(0.1)
        payment_comp = d(resourceId="com.gojek.app:id/2131374409")
        bounds_raw = payment_comp.bounds()
        bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
        d.click(*coordinate_bounds(bounds))

        # choose card
        while not d(resourceId="com.gojek.app:id/2131381956").exists():
            time.sleep(0.2)
        card_comp = d(resourceId="com.gojek.app:id/2131381956")
        bounds_raw = card_comp.bounds()
        bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
        d.click(*coordinate_bounds(bounds))
        d(resourceId="com.gojek.app:id/2131365719").send_keys(card_num)

        expiry_field = d(resourceId="com.gojek.app:id/2131365717")
        expiry_field.click()
        expiry_field.set_text("")
        d.shell(f"input text '{expiry}'")
        d(resourceId="com.gojek.app:id/2131365714").send_keys(cvv)
        # escape keyboard
        d.press("back")
        time.sleep(0.3)
        cfm_button = find_components(d, "save card")
        d.click(*coordinate_bounds(cfm_button["bounds"]))
        while not d(resourceId="btnSubmit").exists():
             time.sleep(0.5)
             if find_components(d, "try again") is not None:
                d.press("back")
                print("card info incorrect")
                return {"status": "failed", "message": "card info incorrect"}
        
        return {"status": "success", "message": "waiting for otp"}
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
def input_payment_otp(otp):
    d = u2.connect()
        # sess = d.session("com.gojek.app") 
    d.app_start("com.gojek.app", stop=False)

    while not d(resourceId="challengeValue").exists():
        time.sleep(0.2)
    d(resourceId="challengeValue").send_keys(otp)
    d(resourceId="btnSubmit").click()

    while not d(resourceId="com.gojek.app:id/2131381956").exists():
        time.sleep(0.5)

    return {"status": "success", "message": "card method added"}
if __name__ == "__main__":
    add_payment("5236 8200 1567 5073", "0630", "035")
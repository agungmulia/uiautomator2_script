# book_ride.py
import threading
import time
import uiautomator2 as u2
from general import check_login_status, find_components, find_components_by_class_text, clear_unexpected_popups, accept_permissions, coordinate_bounds, find_components_by_id, screen_components

def add_card(card_num, expiry, cvv):
    print(f"🚖 Booking ride...")
    try:
        d = u2.connect()
        d.app_start("com.grabtaxi.passenger") 

        while not d(resourceId="com.grabtaxi.passenger:id/node_payment_tag_compose_view").exists():
            time.sleep(0.1)
        time.sleep(0.3)
        payment_comp = d(resourceId="com.grabtaxi.passenger:id/node_payment_tag_compose_view")
        bounds_raw = payment_comp.bounds()
        bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
        d.click(*coordinate_bounds(bounds))
        
        while not find_components(d, "card") is not None:
            time.sleep(0.1)
        card_comp = find_components(d, "card")
        d.click(*coordinate_bounds(card_comp["bounds"]))
        screen_components(d)
        while not d(resourceId="com.grabtaxi.passenger:id/card_number").exists():
            time.sleep(0.1)
        d(resourceId="com.grabtaxi.passenger:id/card_number").send_keys(card_num)
        expiry_field = d(resourceId="com.grabtaxi.passenger:id/card_expiry_date")
        expiry_field.click()
        expiry_field.set_text("")
        d.shell(f"input text '{expiry}'")
        d(resourceId="com.grabtaxi.passenger:id/cvv_number").send_keys(cvv)

        while not find_components(d, "continue") is not None:
             time.sleep(0.2)
        cont_btn = find_components(d, "continue")
        d.click(*coordinate_bounds(cont_btn["bounds"]))

        while not d(resourceId="btnSubmit").exists():
             time.sleep(0.5)
             if find_components(d, "try again") is not None:
                d.press("back")
                print("card info incorrect")
                return {"status": "failed", "message": "card info incorrect"}
        
        # d(resourceId="challengeValue").send_keys("akwowkaokawowak")
        # d(resourceId="btnSubmit").click()
        print("card info added")
        return {"status": "success", "message": "waiting for otp"}
    except Exception as e:
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return str(e)
def input_payment_otp(otp):
    d = u2.connect()
    d.app_start("com.grabtaxi.passenger") 

    while not d(resourceId="challengeValue").exists():
        time.sleep(0.2)
    d(resourceId="challengeValue").send_keys(otp)
    d(resourceId="btnSubmit").click()
    while not find_components(d, "card") is not None:
            time.sleep(0.5)
    return {"status": "success", "message": "card method added"}
if __name__ == "__main__":

        add_card("5236 8200 1567 5073", "0630", "035")
# book_ride.py
import threading
import time
import uiautomator2 as u2
from general import check_login_status, find_components, find_components_by_class_text, clear_unexpected_popups, accept_permissions, coordinate_bounds, find_components_by_id, screen_components

def add_card(card_num, expiry, cvv):
    print(f"🚖 Booking ride...")
    try:
        d = u2.connect()
        d.app_start("com.codigo.comfort") 

        while not find_components(d, "personal") is not None:
            time.sleep(0.1)
        time.sleep(0.3)
        payment_comp = find_components(d, "pay onboard")
        d.click(*coordinate_bounds(payment_comp["bounds"]))
        
        while not find_components(d, "cashless payment") is not None:
            time.sleep(0.1)
        card_comp = find_components(d, "cashless payment")
        d.click(*coordinate_bounds(card_comp["bounds"]))

        while not d(resourceId="imgCreditCard").exists():
            time.sleep(0.1)
        
        add_card_comp = find_components(d, "credit card")
        d.click(*coordinate_bounds(add_card_comp["bounds"]))

        # insert info
        d(resourceId="com.codigo.comfort:id/editText_cardNumber").send_keys(card_num)
        d(resourceId="com.codigo.comfort:id/editText_securityCode").send_keys(cvv)
        d(resourceId="com.codigo.comfort:id/editText_cardHolder").send_keys(cvv)
        expiry_field = d(resourceId="com.codigo.comfort:id/editText_expiryDate")
        expiry_field.click()
        expiry_field.set_text("")
        d.shell(f"input text '{expiry}'")
        time.sleep(0.3)
        d.press("back")

        while not d(resourceId="com.codigo.comfort:id/btnAddCard").exists():
             time.sleep(0.2)
        d(resourceId="com.codigo.comfort:id/btnAddCard").click()

        while not d(resourceId="btnSubmit").exists():
             time.sleep(0.5)
             if find_components(d, "try again") is not None:
                d.press("back")
                print("card info incorrect")
                return {"status": "failed", "message": "card info incorrect"}
        
        print("card info added")
        return {"status": "success", "message": "waiting for otp"}
    except Exception as e:
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return str(e)
def input_payment_otp(otp):
    d = u2.connect()
    d.app_start("com.codigo.comfort") 

    while not d(resourceId="challengeValue").exists():
        time.sleep(0.2)
    d(resourceId="challengeValue").send_keys(otp)
    d(resourceId="btnSubmit").click()
    while not find_components(d, "card") is not None:
            time.sleep(0.5)
    d.press("back")
    while not d(resourceId="imgCreditCard").exists():
         time.sleep(0.2)
    d(resourceId="imgCreditCard").click()
    return {"status": "success", "message": "card method added"}
if __name__ == "__main__":

        # add_card("5236 8200 1567 5073", "0630", "035")
        input_payment_otp("459139")
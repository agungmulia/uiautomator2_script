# book_ride.py
import threading
import time
import uiautomator2 as u2
from general import check_login_status, find_components_by_class_text, clear_unexpected_popups, accept_permissions, coordinate_bounds, find_components_by_id, screen_components

def book_ride_handler(booking_option):
    print(f"🚖 Booking ride...")
    try:
        d = u2.connect()
        d.app_start("com.grabtaxi.passenger") 
        threading.Thread(target=accept_permissions, args=(d,), daemon=True).start()
        threading.Thread(target=clear_unexpected_popups, args=(d,), daemon=True).start()

        # swipe up a bit to show more ride options
        width, height = d.window_size()
        d.swipe(
            width // 2, int(height * 0.55),  # from (middle, 70% height)
            width // 2, int(height * 0.5),  # to (middle, 50% height)
            duration=0.2
        )
        time.sleep(0.5)
        titleComps = find_components_by_id(d, "com.grabtaxi.passenger:id/xsell_confirmation_taxi_type_name")
        # check where the titlecomps[i].text == ride
        for i in range(len(titleComps)):
            if titleComps[i]["text"].lower() == booking_option.lower():
                print("chosen:", titleComps[i]["text"])
                center_x, center_y = coordinate_bounds(titleComps[i]["bounds"])
                d.click(center_x, center_y)
                break
        
        while not d(resourceId="com.grabtaxi.passenger:id/node_payment_tag_compose_view").exists():
            time.sleep(0.1)
        time.sleep(0.3)
        payment_comp = d(resourceId="com.grabtaxi.passenger:id/node_payment_tag_compose_view")
        bounds_raw = payment_comp.bounds()
        bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
        d.click(*coordinate_bounds(bounds))
        
        # # com.grabtaxi.passenger:id/transportBookButton - book button
        d(resourceId="com.grabtaxi.passenger:id/transportBookButton").click()
        time.sleep(0.3)

        # wait for looking for ride
        while not d(resourceId="com.grabtaxi.passenger:id/driverProfileContainer").exists():
            time.sleep(0.1)
            print("wait order")
        print("found driver container, get wait time")
        # close audio protect
        if d(resourceId="com.grabtaxi.passenger:id/btnLeft").exists():
            d(resourceId="com.grabtaxi.passenger:id/btnLeft").click()
        
        time.sleep(0.3)

        wait_time = ""
        if d(text="Driver is nearby").exists():
            wait_time = "driver is nearby"
        
        # find wait time if driver is not nearby
        time_comps = find_components_by_class_text(d, "android.widget.textview", " min")
        print("views:", time_comps)
        if not time_comps is None:
            wait_time = time_comps["text"]

        # cancel button com.grabtaxi.passenger:id/cancelButton
        # choose other reasons, then press anyway
        return {"ride": booking_option, "waiting_time": wait_time, "status": "success"}
    except Exception as e:
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return str(e)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python book_ride.py <destination> <pickup_time>")
    else:
        dest = sys.argv[1]
        time_str = sys.argv[2]
        book_ride_handler(dest, time_str)
# book_ride.py
import threading
import time
import uiautomator2 as u2
from general import clear_unexpected_popups, accept_permissions, coordinate_bounds, find_components_by_id, screen_components, find_components

def cancel_ride():
    print(f"🚖 cancelling ride...")
    try:
        d = u2.connect()
        d.app_start("com.grabtaxi.passenger") 
        threading.Thread(target=accept_permissions, args=(d,), daemon=True).start()
        threading.Thread(target=clear_unexpected_popups, args=(d,), daemon=True).start()

        # scroll to bottom
        d(scrollable=True).scroll.toEnd()
        while not d(resourceId="com.grabtaxi.passenger:id/cancelButton").exists():
            time.sleep(0.1)
        d(resourceId="com.grabtaxi.passenger:id/cancelButton").click()

        # view more first
        while not find_components(d, "other reasons") is not None:
            time.sleep(0.1)
        other_comp = find_components(d, "other reasons")
        d.click(*coordinate_bounds(other_comp["bounds"]))

        while not find_components(d, "anyway") is not None:
            time.sleep(0.1)
        other_comp = find_components(d, "anyway")
        d.click(*coordinate_bounds(other_comp["bounds"]))

        # cancel button com.grabtaxi.passenger:id/cancelButton
        # choose other reasons, then press anyway
        screen_components(d)
        print("📲 Proceeding to book ride...")
    except Exception as e:
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return str(e)

# if __name__ == "__main__":
#     import sys
#     if len(sys.argv) < 3:
#         print("Usage: python book_ride.py <destination> <pickup_time>")
#     else:
#         dest = sys.argv[1]
#         time_str = sys.argv[2]
#         book_ride_handler(dest, time_str)
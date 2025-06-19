# check_price.py
import threading
import time
import uiautomator2 as u2
from general import check_login_status, clear_unexpected_popups, accept_permissions, notify_n8n

def confirmation_check_handler(destination, pickup_time):
    print(f"🚖 Booking ride to {destination} at {pickup_time}...")
    try:
        d = u2.connect()
        sess = d.session("com.grabtaxi.passenger") 
        threading.Thread(target=accept_permissions, args=(d,), daemon=True).start()
        threading.Thread(target=clear_unexpected_popups, args=(d,), daemon=True).start()

        print("testing 1")

        # Call login checker
        if not check_login_status(d):
            raise Exception("User is not logged in. Please log in to continue.")
        
        print("testing 2")

        sess(text="Transport").click()

        time.sleep(2)  # Wait for the UI to update
        sess(text="Where to?").click()
        time.sleep(2)  # Wait for the UI to update
        sess(resourceId="com.grabtaxi.passenger:id/poi_second_search").send_keys(destination)

        time.sleep(2) # Wait for the UI to update
        sess(resourceId="com.grabtaxi.passenger:id/list_item_with_additional_info_container_parent", instance=0).click()

        time.sleep(2) # Wait for the UI to update
        sess(text="Choose This Pickup").click()
        

        # Continue automation like booking ride
        print("📲 Proceeding to book ride...")
    except Exception as e:
        d = u2.connect()
        sess = d.session("org.telegram.messenger") 
        print(f"Error occurred: {e}")
        # notify_n8n("1333039921", e)
        return str(e)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python book_ride.py <destination> <pickup_time>")
    else:
        dest = sys.argv[1]
        time_str = sys.argv[2]
        confirmation_check_handler(dest, time_str)
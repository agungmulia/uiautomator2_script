# book_ride.py
import threading
import time
import uiautomator2 as u2
from general import check_login_status, clear_unexpected_popups, accept_permissions, notify_n8n

def book_ride_handler(booking_option):
    print(f"🚖 Booking ride...")
    try:
        d = u2.connect()
        d.app_start("com.grabtaxi.passenger") 
        threading.Thread(target=accept_permissions, args=(d,), daemon=True).start()
        threading.Thread(target=clear_unexpected_popups, args=(d,), daemon=True).start()

        # Call login checker
        if not check_login_status(d):
            raise Exception("User is not logged in. Please log in to continue.")
        
        option = d(textMatches=f"(?i)^{booking_option}$").click()
        if option.exists(timeout=0.3):
            print(option)
            option.click()
            time.sleep(0.3)


        # Continue automation like booking ride
        print("📲 Proceeding to book ride...")
    except Exception as e:
        d = u2.connect()
        sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        return str(e)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python book_ride.py <destination> <pickup_time>")
    else:
        dest = sys.argv[1]
        time_str = sys.argv[2]
        book_ride_handler(dest, time_str)
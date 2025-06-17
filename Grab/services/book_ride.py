# book_ride.py

import uiautomator2 as u2
import time
from services.general import check_login_status, clear_unexpected_popups, accept_permissions

def book_ride(destination, pickup_time):
    d = u2.connect()
    sess = d.session("com.grabtaxi.passenger") 
    accept_permissions(d)

    time.sleep(2)

    # Call login checker
    if not check_login_status(d):
        print("🔐 Cannot continue without login.")
        return
    
    clear_unexpected_popups(d)

    # Continue automation like booking ride
    print("📲 Proceeding to book ride...")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python book_ride.py <destination> <pickup_time>")
    else:
        dest = sys.argv[1]
        time_str = sys.argv[2]
        book_ride(dest, time_str)
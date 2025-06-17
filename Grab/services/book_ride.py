# book_ride.py

import uiautomator2 as u2
import time
from services.general import check_login_status, clear_unexpected_popups

def main():
    d = u2.connect()
    d.app_start("com.grab.taxibooking")
    time.sleep(5)

    # Call login checker
    if not check_login_status(d):
        print("🔐 Cannot continue without login.")
        return
    
    clear_unexpected_popups(d)

    # Continue automation like booking ride
    print("📲 Proceeding to book ride...")

if __name__ == "__main__":
    main()

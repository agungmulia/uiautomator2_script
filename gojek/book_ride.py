import uiautomator2 as u2
from utils import check_login_status, clear_unexpected_popups, accept_permissions 
def book_ride(destination, pickup_time):
    try:
        d = u2.connect()
        sess = d.session("com.gojek.app") 
        accept_permissions(d)
        clear_unexpected_popups(d)

        # Call login checker
        if not check_login_status(d):
            raise Exception("User is not logged in. Please log in to continue.")
        clear_unexpected_popups(d)
        

        # Continue automation like booking ride
        print("📲 Proceeding to book ride...")
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
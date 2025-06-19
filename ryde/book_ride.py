import uiautomator2 as u2
import time

from tada.utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def book_ride(destination, pickup_time):
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        d.app_start("com.rydesharing.ryde", stop=False)
        
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
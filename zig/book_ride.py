import uiautomator2 as u2
import time

from .utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def book_ride(destination, pickup_time):
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        d.app_start("com.codigo.comfort", stop=False)
        while not d(resourceId="com.codigo.comfort:id/btnBookNow").exists():
            time.sleep(0.1)
        time.sleep(0.2)
        d(resourceId="com.codigo.comfort:id/btnBookNow").click()
        # TODO: check if the book is successful
        
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
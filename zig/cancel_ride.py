import uiautomator2 as u2
import time
from .utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def cancel_ride():
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        d.app_start("com.codigo.comfort", stop=False)
        # cancel trip
        d(scrollable=True).scroll.toEnd()
        while not d(resourceId="com.codigo.comfort:id/btnCancelTrip").exists():
                time.sleep(0.1)
        time.sleep(0.3)
        d(resourceId="com.codigo.comfort:id/btnCancelTrip").click() # cancel
        # TODO: check cancel dropdown options then click then submit
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
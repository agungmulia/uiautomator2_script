import uiautomator2 as u2
import time
from utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def cancel_ride():
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        d.app_start("com.rydesharing.ryde", stop=False)
        while not d(resourceId="com.rydesharing.ryde:id/tv_trip_status").exists():
            time.sleep(0.1)

        d(resourceId="com.rydesharing.ryde:id/btn_cancel").click()

        while not d(resourceId="com.rydesharing.ryde:id/tv_reason").exists():
            time.sleep(0.1)
        
        reasons = find_components_by_id(d, "com.rydesharing.ryde:id/tv_reason")
        for i in range(len(reasons)):
            if reasons[i]["text"].lower() == "others":
                center_x, center_y = coordinate_bounds(reasons[i]["bounds"])
                d.click(center_x, center_y)
                break
        time.sleep(0.1)

        cancel_btn = find_components(d, "cancel booking")
        if cancel_btn is not None:
            center_x, center_y = coordinate_bounds(cancel_btn["bounds"])
            d.click(center_x, center_y)
            
        return {"status": "success", "message": "Ride cancelled!"}

    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
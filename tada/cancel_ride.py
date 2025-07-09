import uiautomator2 as u2
import time
from .utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def cancel_ride():
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        d.app_start("io.mvlchain.tada")

        while not d(resourceId="io.mvlchain.tada:id/rideCancelButton").exists():
            time.sleep(0.1)
        
        d(resourceId="io.mvlchain.tada:id/rideCancelButton").click()

        while not d(resourceId="io.mvlchain.tada:id/reasonRadio").exists():
            time.sleep(0.1)
        cancel_opt = find_components(d, "i found another travel option")
        if cancel_opt is None:
            return {"status": "failed", "message": "no other travel options available"}
        d.click(*coordinate_bounds(cancel_opt["bounds"]))

        while not d(resourceId="io.mvlchain.tada:id/confirmButton").exists():
            time.sleep(0.1)
        d(resourceId="io.mvlchain.tada:id/confirmButton").click()

        while not find_components(d, "cancel ride") is not None:
            time.sleep(0.1)
        time.sleep(0.5)
        cancel_comp = find_components(d, "cancel ride")
        d.click(*coordinate_bounds(cancel_comp["bounds"]))
        response = {"status": "success", "message": "ride cancelled"}
        print(response)
        return response

        
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
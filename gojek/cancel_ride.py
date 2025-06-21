import uiautomator2 as u2
import time
from .utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def cancel_ride():
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        d.app_start("com.gojek.app", stop=False)
        
        screen_components(d)

        # scroll to bottom
        d(scrollable=True).scroll.toEnd()
        time.sleep(1)
        cancel_comp = find_components(d, "cancel booking")
        if cancel_comp is not None:
            cancel_coord = coordinate_bounds(cancel_comp)
            d.click(*cancel_coord)

        time.sleep(0.5)
        cancel_reason_comp = find_components(d, "i found a different transport option")
        if cancel_reason_comp is not None:
            cancel_reason_coord = coordinate_bounds(cancel_reason_comp)
            d.click(*cancel_reason_coord)

        time.sleep(0.5)
        # TODO: check confirm component text
        confirm_comp = find_components(d, "confirm")
        if confirm_comp is not None:
            confirm_coord = coordinate_bounds(confirm_comp)
            d.click(*confirm_coord)

        time.sleep(0.5)
        clear_unexpected_popups(d)
        accept_permissions(d)

    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
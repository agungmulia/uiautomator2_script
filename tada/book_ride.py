import uiautomator2 as u2
import time
import re
from .utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def book_ride(ride):
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        d.app_start("io.mvlchain.tada")
        chosen_comp = find_components(d, ride)
        d.click(*coordinate_bounds(chosen_comp["bounds"]))

        while not find_components(d, "book") is not None:
            time.sleep(0.1)
        book_comp = find_components(d, "book")
        d.click(*coordinate_bounds(book_comp["bounds"]))

        while not d(resourceId="io.mvlchain.tada:id/rideHint").exists():
            time.sleep(1)
        
        wait_time_raw = d(resourceId="io.mvlchain.tada:id/rideHint").get_text()
        match = re.search(r'\d+\s+minutes?', wait_time_raw)
        if match:
            eta_phrase = match.group(0)
            print(f"ETA phrase: {eta_phrase}")
            response = {"ride": ride, "waiting_time": eta_phrase, "status": "success"}
            print(response)
            return response
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return

if __name__ == "__main__":
    book_ride("anytada")
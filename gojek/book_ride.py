import uiautomator2 as u2
import time
from .utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def book_ride(ride, payment_method):
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        d.app_start("com.gojek.app", stop=False)

        # # screen_components(d)
        # choose option
        titleComps = find_components_by_id(d, "com.gojek.app:id/2131378741")
        # check where the titlecomps[i].text == ride
        for i in range(len(titleComps)):
            if titleComps[i]["text"].lower() == ride.lower():
                center_x, center_y = coordinate_bounds(titleComps[i]["bounds"])
                d.click(center_x, center_y)
                break
        # book car
        while not d(resourceId="com.gojek.app:id/tv_title").exists():
            time.sleep(0.1)
        comp = find_components_by_id(d, "com.gojek.app:id/tv_title")
        compCoord = coordinate_bounds(comp[0]["bounds"])
        d.click(compCoord[0], compCoord[1])
        time.sleep(0.3)
        # changed price popup
        changed_priced_comp = find_components(d, "There's a change in price")
        if changed_priced_comp is not None:
            book_comp = find_components(d, "book now")
            center_x, center_y = coordinate_bounds(book_comp["bounds"])
            d.click(center_x, center_y)
            
            print("price changed")
        # com.gojek.app:id/2131381227 waiting time id
        while not d(resourceId="com.gojek.app:id/2131381227").exists():
            time.sleep(0.1)
        waiting_time = d(resourceId="com.gojek.app:id/2131381227").get_text()

        return {"ride": ride, "waiting_time": waiting_time, "status": "success"}
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
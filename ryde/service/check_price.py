import uiautomator2 as u2
import time
import threading
from .utils import select_language, check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def check_price(destination, pickup_time):
    try:
        print("init check price")
        d = u2.connect()
        d.app_start("com.rydesharing.ryde", stop=True)
        while not d(textMatches=r"(?i).*ryde.*").exists():
            time.sleep(0.1)
        threading.Thread(target=accept_permissions, args=(d,), daemon=True).start()
        threading.Thread(target=clear_unexpected_popups, args=(d,), daemon=True).start()
        # select language
        select_language(d)

        if not check_login_status(d):
            print("User is not logged in. Please log in to continue.")
            return
        print("📲 Proceeding to book ride...")
        d(text="Where to?").click()
        while not d(text="Enter dropoff location").exists():
            time.sleep(0.1)

        # # mock location
        # start_comp = find_components_by_id(d, "com.rydesharing.ryde:id/tv_start")[0]
        # d.click(*coordinate_bounds(start_comp["bounds"]))
        # loc_comp = find_components(d, "british council (napier road centre)")
        # d.click(*coordinate_bounds(loc_comp["bounds"]))
        
        d(resourceId="com.rydesharing.ryde:id/tv_stop").send_keys(destination)
        # pick the 1st element in the list
        # while not d(resourceId="com.rydesharing.ryde:id/tv_address").exists():
        #     print("waiting list")
        #     time.sleep(0.1)
        time.sleep(1)
        drop_comps = find_components_by_id(d, "com.rydesharing.ryde:id/tv_name")
        if drop_comps is not None:
            drop_comp = drop_comps[0]
            d.click(*coordinate_bounds(drop_comp["bounds"]))
        while not d(resourceId="com.rydesharing.ryde:id/btn_confirm").exists():
            time.sleep(0.1)
        d(resourceId="com.rydesharing.ryde:id/btn_confirm").click()

        # swipe for full ride options from 1/3 screens height
        width, height = d.window_size()
        d.swipe(
            width // 2, int(height * 0.55),  # from (middle, 70% height)
            width // 2, int(height * 0.5),  # to (middle, 50% height)
            duration=0.1
        )
        time.sleep(0.3)

        title_comps = find_components_by_id(d, "com.rydesharing.ryde:id/tv_service")
        desc_comps = find_components_by_id(d, "com.rydesharing.ryde:id/tv_service_desc")
        price_comps = find_components_by_id(d, "com.rydesharing.ryde:id/tv_price")

        result = []
        for i in range(len(title_comps)):
            result.append({
                "title": title_comps[i]["text"],
                "desc": desc_comps[i]["text"],
                "price": price_comps[i]["text"]
            })
        print(result)
        return result
        
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
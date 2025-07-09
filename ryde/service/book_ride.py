import uiautomator2 as u2
import time

from .utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def book_ride(ride):
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        d.app_start("com.rydesharing.ryde", stop=False)
        while not d(resourceId="com.rydesharing.ryde:id/tv_service").exists():
            time.sleep(0.1)
        titles = find_components_by_id(d, "com.rydesharing.ryde:id/tv_service")
        for i in range(len(titles)):
            print(titles[i]["text"].lower(), "==", ride.lower())
            if ride.lower() == "rydex":
                # swipe down a bit
                width, height = d.window_size()
                d.swipe(
                    width // 2, int(height * 0.5),  # from (middle, 70% height)
                    width // 2, int(height * 0.55),  # to (middle, 50% height)
                    duration=0.2
                )
                break
            if titles[i]["text"].lower()  == ride.lower() and ride.lower() != "rydex":
                print("chosen:", titles[i]["text"] )
                center_x, center_y = coordinate_bounds(titles[i]["bounds"])
                d.click(center_x, center_y)
                break

        while not d(resourceId="com.rydesharing.ryde:id/btn_book").exists():
            time.sleep(0.1)
        time.sleep(0.2)
        d(resourceId="com.rydesharing.ryde:id/btn_book").click()

        while not d(resourceId="com.rydesharing.ryde:id/tv_trip_status").exists():
            time.sleep(0.1)

        wait_time = "driver is on the way"

        return {"ride": ride, "waiting_time": wait_time, "status": "success"}
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
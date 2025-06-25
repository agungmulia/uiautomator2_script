import uiautomator2 as u2
import time

from .utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def book_ride(ride):
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        d.app_start("com.codigo.comfort", stop=False)
        # choose ride option
        fareDescs = find_components_by_id(d, "com.codigo.comfort:id/tvFareDescription")
        fareSubDescs = find_components_by_id(d, "com.codigo.comfort:id/tvFareSubDescription")
        for i in range(len(fareDescs)):
            print(fareDescs[i]["text"].lower() + fareSubDescs[i]["text"].lower(), "==", ride.lower())
            if fareDescs[i]["text"].lower() + fareSubDescs[i]["text"].lower() == ride.lower():
                print("chosen:", fareDescs[i]["text"] + fareSubDescs[i]["text"])
                center_x, center_y = coordinate_bounds(fareDescs[i]["bounds"])
                d.click(center_x, center_y)
                break

        while not d(resourceId="com.codigo.comfort:id/btnBookNow").exists():
            time.sleep(0.1)
        time.sleep(0.2)
        d(resourceId="com.codigo.comfort:id/btnBookNow").click()
        # new UiSelector().resourceId("com.codigo.comfort:id/tvTimeEstimated")
        while not d(resourceId="com.codigo.comfort:id/tvTimeEstimated").exists():
            time.sleep(0.1)
        time.sleep(0.2)

        wait_time = d(resourceId="com.codigo.comfort:id/tvTimeEstimated").get_text()
        print("wait time:", wait_time)

        return {"ride": ride, "waiting_time": wait_time, "status": "success"}


        # # TODO: check if the book is successful
        
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
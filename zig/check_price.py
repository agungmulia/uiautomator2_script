import uiautomator2 as u2
import time
import re
from .utils import select_language, check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds, find_components_by_drawing_order
def check_price(destination, pickup_time):
    try:
        print("init check price")
        d = u2.connect()
        d.app_start("com.codigo.comfort", stop=True)
        time.sleep(1)
        clear_unexpected_popups(d)
        # select language
        accept_permissions(d)

        select_language(d)

        if not check_login_status(d):
            print("User is not logged in. Please log in to continue.")
            return {"status": "not_logged_in", "message": "User is not logged in. Please log in to continue."}
        clear_unexpected_popups(d)

        # proceed book
        print("proceed booking zig")
        ride_comp = find_components(d, "car rides")
        if ride_comp is not None:
            ride_coord = coordinate_bounds(ride_comp["bounds"])
            d.click(*ride_coord)
        while not d(resourceId="txtInputDestination").exists():
            print("input destination")
            time.sleep(0.1)
        # time.sleep(0.2)
        d(resourceId="txtInputDestination").click()
        
        while not d(text="Where to?").exists():
            print("where to")
            time.sleep(0.1)
        # time.sleep(0.3)
        d(text="Where to?").send_keys(destination)

        # choose first element in the search list
        while not d(resourceId="com.codigo.comfort:id/lblRecentLocationAddress").exists():
            time.sleep(0.1)
        # time.sleep(0.5)
        search_res_comps = find_components_by_id(d, "com.codigo.comfort:id/lblRecentLocationAddress")
        if search_res_comps is not None:
            search_res_comp = search_res_comps[0]
            search_res_coord = coordinate_bounds(search_res_comp["bounds"])
            d.click(*search_res_coord)

        # # confirm pick up
        while not d(resourceId="btnConfirmPickUp").exists():
            time.sleep(0.1)
        # time.sleep(0.5)
        d(resourceId="btnConfirmPickUp").click()


        while not d(resourceId="com.codigo.comfort:id/tvApplicableFare").exists():
            time.sleep(0.1)
        # time.sleep(0.5)

        fareDescs = find_components_by_id(d, "com.codigo.comfort:id/tvFareDescription")
        fareSubDescs = find_components_by_id(d, "com.codigo.comfort:id/tvFareSubDescription")
        fares = find_components_by_id(d, "com.codigo.comfort:id/tvApplicableFare")
        # # make a dict with title and price field, where title is fareDesc + fareSubDesc
        rides = []
        for i in range(len(fareDescs)):
            rides.append({
                "title": fareDescs[i]["text"] + fareSubDescs[i]["text"],
                "price": fares[i]["text"]
            })
        return rides

        # while not d(resourceId="com.codigo.comfort:id/btnBookNow").exists():
        #     time.sleep(0.1)
        # time.sleep(0.2)
        # d(resourceId="com.codigo.comfort:id/btnBookNow").click()

        # cancel trip
        # d(scrollable=True).scroll.toEnd()
        # while not d(resourceId="com.codigo.comfort:id/btnCancelTrip").exists():
        #         time.sleep(0.1)
        # time.sleep(0.3)
        # d(resourceId="com.codigo.comfort:id/btnCancelTrip").click() # cancel
        # TODO: check cancel dropdown options then click then submit


    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to check price: {e}")
        return
    
def is_single_price(text):
    # Count how many float numbers are in the text
    matches = re.findall(r"\d+\.\d+", text)
    return len(matches) == 1  # Only keep if there's exactly one price

def extract_price(text):
    match = re.search(r"\d+\.\d+", text)
    return float(match.group()) if match else float('inf')
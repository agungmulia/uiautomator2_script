import uiautomator2 as u2
import time
import re
from utils import select_language, check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds, find_components_by_drawing_order
def check_price(destination, pickup_time):
    try:
        print("init check price")
        d = u2.connect()
        d.app_start("com.codigo.comfort", stop=False)
        time.sleep(2)
        clear_unexpected_popups(d)
        # select language
        accept_permissions(d)
        print("debug screen components")

        # screen_components(d)
        
        select_language(d)

        if not check_login_status(d):
            print("User is not logged in. Please log in to continue.")
            return 
        clear_unexpected_popups(d)

        # proceed book
        print("proceed booking")
        ride_comp = find_components(d, "car rides")
        if ride_comp is not None:
            ride_coord = coordinate_bounds(ride_comp["bounds"])
            d.click(*ride_coord)
        if not d(resourceId="txtInputDestination").exists():
            time.sleep(0.1)
        time.sleep(0.5)
        d(resourceId="txtInputDestination").click()
        
        if not d(text="Where to?").exists():
            time.sleep(0.1)
        time.sleep(0.3)
        d(text="Where to?").send_keys(destination)
        screen_components(d)

        # choose first element in the search list
        if not d(resourceId="com.codigo.comfort:id/lblRecentLocationAddress").exists():
            time.sleep(0.1)
        time.sleep(0.5)
        search_res_comps = find_components_by_id(d, "com.codigo.comfort:id/lblRecentLocationAddress")
        if search_res_comps is not None:
            search_res_comp = search_res_comps[0]
            search_res_coord = coordinate_bounds(search_res_comp["bounds"])
            d.click(*search_res_coord)

        # # confirm pick up
        if not d(resourceId="btnConfirmPickUp").exists():
            time.sleep(0.1)
        time.sleep(0.5)
        d(resourceId="btnConfirmPickUp").click()


        # choose cheapest fare
        fare_comps = find_components_by_id(d, "com.codigo.comfort:id/tvApplicableFare")
        # Filter to only those with single-price format
        single_price_comps = [c for c in fare_comps if is_single_price(c["text"])]
        # Get the one with the lowest price
        cheapest = min(single_price_comps, key=lambda x: extract_price(x["text"]))
        print(coordinate_bounds(cheapest["bounds"]))
        center_x, center_y = coordinate_bounds(cheapest["bounds"])
        d.click(center_x, center_y)
        print({
            "price": extract_price(cheapest["text"]),
            "pickup_time": pickup_time
        })
        return {
            "ride": "Zig",
            "price": extract_price(cheapest["text"])
        }

        
        




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
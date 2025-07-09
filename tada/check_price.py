import uiautomator2 as u2
import time
import xml.etree.ElementTree as ET
import traceback

from .utils import select_language, check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def check_price(destination, pickup_time):
    try:
        print("init check price")
        d = u2.connect()
        d.app_start("io.mvlchain.tada", stop=True)
        time.sleep(2)
        # select language
        accept_permissions(d)

        select_language(d)

        if not check_login_status(d):
            print("User is not logged in. Please log in to continue.")
            return {"status": "not_logged_in", "message": "User is not logged in. Please log in to continue."}
        
        while not find_components(d, "where to") is not None:
            time.sleep(0.1)
        where_to_comp = find_components(d, "where to")
        d.click(*coordinate_bounds(where_to_comp["bounds"]))

        while not d(className="android.widget.EditText").exists():
            time.sleep(0.1)
        
        d(className="android.widget.EditText")[1].send_keys(destination)
        while not d(description="tada search place image")[0].exists():
            time.sleep(0.1)
        pick_comp = d(description="tada search place image")[0]
        pick_comp_bounds_raw = pick_comp.bounds()
        bounds = f"[{pick_comp_bounds_raw[0]},{pick_comp_bounds_raw[1]}][{pick_comp_bounds_raw[2]},{pick_comp_bounds_raw[3]}]"

        d.click(*coordinate_bounds(bounds))

        # button set pick up location
        while not find_components(d, "set pickup location") is not None:
            if find_components(d, "set destination location") is not None:
                d.click(*coordinate_bounds(find_components(d, "set destination location")["bounds"]))
            time.sleep(0.1)
        set_pickup_comp = find_components(d, "set pickup location")
        d.click(*coordinate_bounds(set_pickup_comp["bounds"]))

        while not find_components(d, "anytada"):
            time.sleep(0.1)
        
        time.sleep(0.3)
        d.swipe(0.5, 0.75, 0.70, 0.5, duration=0.1)
        time.sleep(0.5)

        xml = d.dump_hierarchy()
        root = ET.fromstring(xml)
        ride_list_raw = traverse(root)

        rides = []
        for ride in ride_list_raw:
            title = ride[0]
            price = ride[4]
            rides.append({"title": title, "price": price})
        print(rides)
        return rides
    except Exception as e:
        print("error raised on ryde check price")
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        traceback.print_exc()
        print(f"[Error] Failed to book ride: {e}")
        return

def traverse(node, parent=None):
    results = []
    class_name = node.attrib.get('class', '')
    content_desc = node.attrib.get('content-desc', '')

    if content_desc == 'car image' and class_name == 'android.view.View':
        sibling_texts = []

        # Get all sibling texts if available
        if parent is not None:
            for sibling in parent:
                if sibling is not node:
                    text = sibling.attrib.get('text')
                    if text:
                        sibling_texts.append(text)

        results.append(sibling_texts)

    # Traverse children recursively
    for child in node:
        results.extend(traverse(child, node))

    return results

if __name__ == "__main__":
    check_price("plaza singapura", "now")
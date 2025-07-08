import uiautomator2 as u2
import xml.etree.ElementTree as ET
import time
from .utils import check_login_status, clear_unexpected_popups, accept_permissions, find_components_by_class_text, screen_components, find_components, find_components_by_id, coordinate_bounds
from general import cache_get, cache_set
def check_price(restaurant, dropoff, orders, note= ""):
    try:
        d = u2.connect()
        d.app_start("com.global.foodpanda.android", stop=False)
        # d.app_start("com.global.foodpanda.android", stop=True)
        # time.sleep(2)
        # accept_permissions(d)
        # clear_unexpected_popups(d)
        # Call login checker
        # if not check_login_status(d):
        #     return {"status": "not_logged_in", "message": "User is not logged in. Please log in to continue."}
        
        while not d(resourceId="HomeSearchBar").exists():
            time.sleep(0.5)
        print("klik search")
        search_bar = d(resourceId="HomeSearchBar")
        bounds_raw = search_bar.bounds()
        bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
        d.click(*coordinate_bounds(bounds))

        search = d(className="android.widget.EditText")[0]
        search.send_keys(restaurant)

        while not find_components(d, "in restaurants"):
            time.sleep(0.1)

        # pick in restaurant
        restaurant_comp = find_components(d, "in restaurants")
        if restaurant_comp is not None:
            d.click(*coordinate_bounds(restaurant_comp["bounds"]))
        
        while not d(resourceId="TITLE").exists():
            time.sleep(0.1)
        d(resourceId="TITLE").click()
        result = []
        for idx, order in enumerate(orders):
            while not d(resourceId="search_bar").exists():
                time.sleep(0.1)
                print("waiting for search bar")
            time.sleep(0.4)
            d(resourceId="search_bar").click()

            while not d(resourceId="com.global.foodpanda.android:id/searchEditText").exists():
                time.sleep(0.2)
            d(resourceId="com.global.foodpanda.android:id/searchEditText").send_keys(order["name"])

            while not d(resourceId="com.global.foodpanda.android:id/titleTextView").exists():
                time.sleep(0.2)
            # # d.hide_keyboard()
            d(resourceId="com.global.foodpanda.android:id/dishTileLayout").click()
            # # we can display the list then ask user
            # get all the menu
            while True:
                swipe_end_comp = find_components_by_class_text(d, "android.widget.textview", "bought together")
                if swipe_end_comp is not None:
                    break
                d.swipe(0.5, 0.57, 0.5, 0.5, duration=0.05)
           
            if order["pref"] == "regular":
                if order["pcs"] > 1:
                    button_add = d(className="android.widget.Button")[2]
                    for i in range(order["pcs"] - 1):
                        # convert bound to [x,y][x,y]
                        bounds_raw = button_add.bounds()
                        bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"

                        d.click(*coordinate_bounds(bounds))
                time.sleep(0.2)
                d(className="android.widget.Button")[3].click()
                if idx != len(orders) - 1:
                    time.sleep(0.2)
                    d.press("back")
                else:
                    while not d(resourceId="com.global.foodpanda.android:id/primaryActionButton").exists():
                        time.sleep(0.2)
                    d(resourceId="com.global.foodpanda.android:id/primaryActionButton").click()
                    while not d(resourceId="DhBreakdownCtaButton").exists():
                        time.sleep(0.1)
                    d(resourceId="DhBreakdownCtaButton").click()
                    res = get_order_detail(d)
                    return {"status": "success","price": res["total_price"], "orders": res["orders"], "app": "foodpanda"}

                    
            else:
                

                # Parse dump
                xml = d.dump_hierarchy()
                root = ET.fromstring(xml)
                special_request = traverse(root)
                result.append(special_request)
                d.press("back")
                time.sleep(0.2)
                d.press("back")
        

        # specialReqcomp = d(textMatches="(?i).*special request.*").exists()
        # print("special req: ", specialReqcomp)
        print(result)
        cache_set("food_order", {
            "restaurant": restaurant,
            "dropoff": dropoff,
            "orders": orders,
            "note": note
        })
        return result
       
    #    order = [{
    #     "name": order,
    #     "is_general_name": true,
    #     "pcs": pcs,
    #     "pref": pref,
    #     "note": note
    # }]
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
def confirm_order(special_requests):
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        d.app_start("com.global.foodpanda.android", stop=False)
        order_detail = cache_get("food_order")
        print("cache cek",order_detail)
        if order_detail is None:
            return {"error": "No order details found in cache."}
        
        for idx,order in enumerate(order_detail["orders"]):
            while not d(resourceId="search_bar").exists():
                time.sleep(0.1)
                print("waiting for search bar")
            time.sleep(0.4)
            d(resourceId="search_bar").click()

            while not d(resourceId="com.global.foodpanda.android:id/searchEditText").exists():
                time.sleep(0.1)
            d(resourceId="com.global.foodpanda.android:id/searchEditText").send_keys(order["name"])

            while not d(resourceId="com.global.foodpanda.android:id/titleTextView").exists():
                time.sleep(0.1)
            # # d.hide_keyboard()
            d(resourceId="com.global.foodpanda.android:id/dishTileLayout").click()
            # # we can display the list then ask user
            # get all the menu
            while True:
                swipe_end_comp = find_components_by_class_text(d, "android.widget.textview", "bought together")
                if swipe_end_comp is not None or find_components_by_class_text(d, "android.widget.textview", "not available"):
                    break
                d.swipe(0.5, 0.57, 0.5, 0.5, duration=0.05)
            for req in special_requests[idx]:
                chosen = find_components(d, req)
                if chosen is not None:
                    d.click(*coordinate_bounds(chosen["bounds"]))
                    print("click req: ", req)

            if order["pcs"] > 1:
                button_add = d(className="android.widget.Button")[2]
                for i in range(order["pcs"] - 1):
                    # convert bound to [x,y][x,y]
                    bounds_raw = button_add.bounds()
                    bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"

                    d.click(*coordinate_bounds(bounds))
                    d(className="android.widget.Button")[3].click()
            print(len(order_detail["orders"]) - 1)
            print("loop",idx)
            if idx != len(order_detail["orders"]) - 1:
                d.press("back")
                d.press("back")
                time.sleep(0.2)
                continue
        while not d(resourceId="com.global.foodpanda.android:id/primaryActionButton").exists():
            time.sleep(0.1)
        d(resourceId="com.global.foodpanda.android:id/primaryActionButton").click()
        while not d(resourceId="DhBreakdownCtaButton").exists():
            time.sleep(0.1)
        d(resourceId="DhBreakdownCtaButton").click()

        get_order_detail(d)

        

    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to confirm_order: {e}")
        return 
    

def traverse(node, parent=None, grandparent=None):
    results = []
    class_name = node.attrib.get('class', '')

    if class_name == 'android.widget.CheckBox':
        sibling_text = None
        parent_sibling_text = None

        # Get one sibling text if available
        if parent is not None:
            for s in list(parent):
                if s is not node:
                    t = s.attrib.get('text')
                    if t:
                        sibling_text = t
                        break

        # Get one parent sibling text if available
        if grandparent is not None and parent is not None:
            for p in list(grandparent):
                if p is not parent:
                    t = p.attrib.get('text')
                    if t:
                        parent_sibling_text = t
                        break

        # Append current checkbox data
        results.append(
            {
                "request": sibling_text,
                "price": parent_sibling_text,
            }
        )

    # Traverse children recursively
    for child in node:
        results.extend(traverse(child, node, parent))

    return results


def get_order_detail(d):
    while True:
        swipe_end_comp = find_components_by_class_text(d, "android.widget.textview", "apply a voucher")
        if swipe_end_comp is not None:
            break
        d.swipe(0.5, 0.57, 0.5, 0.5, duration=0.05)
    # check voucher
    d(resourceId="com.global.foodpanda.android:id/applyVoucherTextView").click()
    time.sleep(0.9)
    el = d(description="Apply")[1]
    bounds_raw = el.bounds()
    bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
    d.click(*coordinate_bounds(bounds))
    time.sleep(2)
    if not d(resourceId="com.global.foodpanda.android:id/productItemNameTextView").exists():
        d.press("back")
        d.press("back")
    time.sleep(0.8)

    order_name_comps = find_components_by_id(d, "com.global.foodpanda.android:id/productItemNameTextView")
    order_price_comps = find_components_by_id(d, "com.global.foodpanda.android:id/productItemPriceTextView")
    orders = []
    for i in range(len(order_name_comps)):
        orders.append({
            "name": order_name_comps[i]["text"],
            "price": order_price_comps[i]["text"]
        })
    while not d(resourceId="com.global.foodpanda.android:id/priceTextView").exists():
            time.sleep(0.1)
    price = d(resourceId="com.global.foodpanda.android:id/priceTextView").get_text()
    
    print({
        "total_price": price,
        "orders": orders
        
    })
    return {
        "total_price": price,
        "orders": orders
    }

if __name__ == "__main__":
    # Example usage
    restaurant = "McDonald's"
    dropoff = "Your Address"
    orders = [{
        "name": "buttermilk",
        "is_general_name": True,
        "pcs": 2,
        "pref": "regular",
        "note": "No special request"
    }, 
    {
        "name": "big ma",
        "is_general_name": True,
        "pcs": 2,
        "pref": "regular",
        "note": "No special request"
    }
    ]
    
    check_price(restaurant, dropoff, orders)
    special_reqs = [[ "no pineapple", "no black pepper mayo" ], ["no bigmac sauce", "no onion"]]
    # special_reqs = [[ "no cheese" ], ["no cheese", "no curry sauce"]]
    # confirm_order(special_requests=special_reqs)

import uiautomator2 as u2
import xml.etree.ElementTree as ET
import time
from .utils import check_login_status, clear_unexpected_popups, accept_permissions, find_components_by_class_text, screen_components, find_components, find_components_by_id, coordinate_bounds
from general import cache_get, cache_set
def check_price(restaurant, dropoff, orders, note= ""):
    try:
        d = u2.connect()
        # d.app_start("com.deliveroo.orderapp", stop=False)
        d.app_start("com.deliveroo.orderapp", stop=False)
        # time.sleep(4)
        # accept_permissions(d)
        # clear_unexpected_popups(d)
        # # Call login checker
        # if not check_login_status(d):
        #     return {"status": "not_logged_in", "message": "User is not logged in. Please log in to continue."}
        if d(description="Search restaurants and cuisines").exists():
            el = d(description="Search restaurants and cuisines")
            bounds_raw = el.bounds()
            bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
            d.click(*coordinate_bounds(bounds))
            time.sleep(0.5)
        d.shell(f"input text '{restaurant}'")
        d.press("enter")
        
        while not d(resourceId="com.deliveroo.orderapp:id/card_image").exists():
            time.sleep(0.2)
        el = d(resourceId="com.deliveroo.orderapp:id/card_image")[0]
        bounds_raw = el.bounds()
        bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
        d.click(*coordinate_bounds(bounds))
        time.sleep(0.3)
        press_by_desc(d, "Search")

        for idx, order in enumerate(orders):
            # if order["pref"] == "regular":
            #     press_by_desc(d, "Regular")
            # else:
            d.shell(f"input text '{order['name']}'")
            d.press("enter")
            time.sleep(0.3)
            if order["pref"] == "regular":
                while not d(resourceId="com.deliveroo.orderapp:id/item_name").exists():
                    time.sleep(0.2)
                lists = d(resourceId="com.deliveroo.orderapp:id/item_name")
                # check who has the shortest text
                chosen = lists[0]
                for el in lists:
                    el_length = len(el.get_text())
                    if el_length < len(chosen.get_text()):
                        chosen = el
                bounds_raw = chosen.bounds()
                bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
                d.click(*coordinate_bounds(bounds))
                
                while not d(resourceId="com.deliveroo.orderapp:id/increment_quantity").exists():
                    time.sleep(0.2)
                    print("waiting for quantity increment")
                if order["pcs"] != 1:
                    print("pcs", order["pcs"])
                    for i in range(order["pcs"] - 1):
                        d(resourceId="com.deliveroo.orderapp:id/increment_quantity").click()
                # add to basket
                d(resourceId="com.deliveroo.orderapp:id/modifier_cta_button").click()

                if idx != len(orders) - 1:
                    while not d(resourceId="com.deliveroo.orderapp:id/input").exists():
                        time.sleep(0.2)
                    d(resourceId="com.deliveroo.orderapp:id/input").click()
                    d(resourceId="com.deliveroo.orderapp:id/input").set_text("")
                else:
                    while not d(resourceId="com.deliveroo.orderapp:id/button_view_basket").exists():
                        time.sleep(0.2)
                    d(resourceId="com.deliveroo.orderapp:id/button_view_basket").click()

                    # # find voucher button
                    while not d(description="View credit and vouchers").exists():
                        d.swipe(0.5, 0.57, 0.5, 0.5, duration=0.05)
                    press_by_desc(d, "View credit and vouchers")
                    time.sleep(1)
                    if find_components(d, "No credit just yet") is not None:
                        d.press("back")
                        time.sleep(0.5)
                    else:
                        d.press("back")
                    lists = d(textContains="$")
                    # get last element
                    price = lists[len(lists) - 1].get_text()
                    
                    print("price", price)
                    return {"status": "success","price": price, "orders": orders, "app": "deliveroo"}

                    
                # press_by_id(d, "com.deliveroo.orderapp:id/item_image")
            #         return {"status": "success","price": res["total_price"], "orders": res["orders"], "app": "foodpanda"}

                    
            # else:
                

            #     # Parse dump
            #     xml = d.dump_hierarchy()
            #     root = ET.fromstring(xml)
            #     special_request = traverse(root)
            #     result.append(special_request)
            #     d.press("back")
            #     time.sleep(0.2)
            #     d.press("back")
        
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to order food: {e}")
        return
# def confirm_order(special_requests):
#     try:
#         d = u2.connect()
#         # sess = d.session("com.gojek.app") 
#         d.app_start("com.deliveroo.orderapp", stop=False)
#         order_detail = cache_get("food_order")
#         print("cache cek",order_detail)
#         if order_detail is None:
#             return {"error": "No order details found in cache."}
        
#         for idx,order in enumerate(order_detail["orders"]):
#             while not d(resourceId="search_bar").exists():
#                 time.sleep(0.1)
#                 print("waiting for search bar")
#             time.sleep(0.4)
#             d(resourceId="search_bar").click()

#             while not d(resourceId="com.deliveroo.orderapp:id/searchEditText").exists():
#                 time.sleep(0.1)
#             d(resourceId="com.deliveroo.orderapp:id/searchEditText").send_keys(order["name"])

#             while not d(resourceId="com.deliveroo.orderapp:id/titleTextView").exists():
#                 time.sleep(0.1)
#             # # d.hide_keyboard()
#             d(resourceId="com.deliveroo.orderapp:id/dishTileLayout").click()
#             # # we can display the list then ask user
#             # get all the menu
#             while True:
#                 swipe_end_comp = find_components_by_class_text(d, "android.widget.textview", "bought together")
#                 if swipe_end_comp is not None or find_components_by_class_text(d, "android.widget.textview", "not available"):
#                     break
#                 d.swipe(0.5, 0.57, 0.5, 0.5, duration=0.05)
#             for req in special_requests[idx]:
#                 chosen = find_components(d, req)
#                 if chosen is not None:
#                     d.click(*coordinate_bounds(chosen["bounds"]))
#                     print("click req: ", req)

#             if order["pcs"] > 1:
#                 button_add = d(className="android.widget.Button")[2]
#                 for i in range(order["pcs"] - 1):
#                     # convert bound to [x,y][x,y]
#                     bounds_raw = button_add.bounds()
#                     bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"

#                     d.click(*coordinate_bounds(bounds))
#                     d(className="android.widget.Button")[3].click()
#             print(len(order_detail["orders"]) - 1)
#             print("loop",idx)
#             if idx != len(order_detail["orders"]) - 1:
#                 d.press("back")
#                 d.press("back")
#                 time.sleep(0.2)
#                 continue
#         while not d(resourceId="com.deliveroo.orderapp:id/primaryActionButton").exists():
#             time.sleep(0.1)
#         d(resourceId="com.deliveroo.orderapp:id/primaryActionButton").click()
#         while not d(resourceId="DhBreakdownCtaButton").exists():
#             time.sleep(0.1)
#         d(resourceId="DhBreakdownCtaButton").click()

#         get_order_detail(d)

        

#     except Exception as e:
#         # d = u2.connect()
#         # sess = d.session("org.telegram.messenger") 
#         # notify_n8n("1333039921", e)
#         print(f"[Error] Failed to confirm_order: {e}")
#         return 
    
def checkout():
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        d.app_start("com.deliveroo.orderapp", stop=False)
        # press_by_text(d, "Go to checkout")
        # time.sleep(1)
        if find_components(d, "go to checkout") is not None:
            press_by_text(d, "Go to checkout")
        while not find_components(d, "how would you like to pay?") is not None:
            time.sleep(0.2)
        if find_components(d, "choose a payment method") is not None:
            print("choose a payment method")
            return {"status": "no_payment_default", "message": "No payment method available"}
        d(scrollable=True).scroll.toEnd()
        time.sleep(0.5)
        if d(text="Add a new address").exists():
            print("no address")
            return {"status": "no_address_default", "message": "No address available"}
        press_by_text(d, "Place delivery order")
        return {"status": "success", "waiting_time": ""}
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to checkout: {e}")
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
    order_name_comps = find_components_by_id(d, "com.deliveroo.orderapp:id/productItemNameTextView")
    order_price_comps = find_components_by_id(d, "com.deliveroo.orderapp:id/productItemPriceTextView")
    orders = []
    for i in range(len(order_name_comps)):
        orders.append({
            "name": order_name_comps[i]["text"],
            "price": order_price_comps[i]["text"]
        })
    while not d(resourceId="com.deliveroo.orderapp:id/priceTextView").exists():
            time.sleep(0.1)
    price = d(resourceId="com.deliveroo.orderapp:id/priceTextView").get_text()
    
    print({
        "total_price": price,
        "orders": orders
        
    })
    return {
        "total_price": price,
        "orders": orders
    }

def press_by_id(d, id):
    while not d(resourceId=id).exists():
        time.sleep(0.2)
    el = d(resourceId=id)[0]
    bounds_raw = el.bounds()
    bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
    d.click(*coordinate_bounds(bounds))    

def press_by_text(d, txt):
    while not d(text=txt).exists():
        time.sleep(0.2)
    el = d(text=txt)
    bounds_raw = el.bounds()
    bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
    d.click(*coordinate_bounds(bounds))    

def press_by_desc(d, desc):
    while not d(description=desc).exists():
        time.sleep(0.2)
    el = d(description=desc)[0]
    bounds_raw = el.bounds()
    bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
    d.click(*coordinate_bounds(bounds))

if __name__ == "__main__":
    # Example usage
    restaurant = "McDonald"
    dropoff = "Your Address"
    orders = [
    {
        "name": "big mac",
        "is_general_name": True,
        "pcs": 2,
        "pref": "regular",
        "note": "No special request"
    },
    {
        "name": "oatside",
        "is_general_name": True,
        "pcs": 1,
        "pref": "regular",
        "note": "No special request"
    }
    ]
    
    # check_price(restaurant, dropoff, orders)
    checkout()
    # special_reqs = [[ "no pineapple", "no black pepper mayo" ], ["no bigmac sauce", "no onion"]]
    # # special_reqs = [[ "no cheese" ], ["no cheese", "no curry sauce"]]
    # confirm_order(special_requests=special_reqs)

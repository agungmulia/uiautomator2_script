import threading
import time
import uiautomator2 as u2
import xml.etree.ElementTree as ET
import traceback
from general import find_components, coordinate_bounds, cache_get, cache_set, find_components_by_id, accept_permissions, clear_unexpected_popups, check_login_status

def check_order_food(restaurant, dropoff, orders, note=""):
    try:
        d = u2.connect()
        d.app_start("com.grabtaxi.passenger", stop=True) 
        threading.Thread(target=accept_permissions, args=(d,), daemon=True).start()
        threading.Thread(target=clear_unexpected_popups, args=(d,), daemon=True).start()


        # Call login checker
        # if not check_login_status(d):
        #     return {"status": "not_logged_in", "message": "User is not logged in. Please log in to continue."}
        
        while not d(text="Food").exists():
            time.sleep(0.2)
        d(text="Food").click()

        while not d(text="What shall we deliver?").exists():
            time.sleep(0.2)
        d(text="What shall we deliver?").click()
        while not d(resourceId="com.grabtaxi.passenger:id/gds_appbar_search_field").exists():
                time.sleep(0.2)
        print(d(text="Would you like to eat something?").exists())
        time.sleep(0.5)
        d(className="android.widget.EditText").send_keys(restaurant)
        # pick 1st element
        while not d(className="android.view.View")[14].exists():
            time.sleep(0.2)
            print("wait for search result")
            # com.grabtaxi.passenger:id/deliveries_search_autocomplete
        print("click search result")
        d(className="android.view.View")[14].click()
        while not d(resourceId="com.grabtaxi.passenger:id/universal_merchant_card_compose_view").exists():
                time.sleep(0.2)
        # avoid ads
        if not d(text="Ad").exists():
            d(resourceId="com.grabtaxi.passenger:id/universal_merchant_card_compose_view")[0].click()
        else:
            d(resourceId="com.grabtaxi.passenger:id/universal_merchant_card_compose_view")[1].click()
        time.sleep(0.5)
        specials = []
        for idx, order in enumerate(orders):
            print("loop order", order["name"])
            while not d(resourceId="com.grabtaxi.passenger:id/shortcutComposeContainer").exists():
                print("skrol")
                d.swipe(0.5, 0.7, 0.5, 0.5, duration=0.2)

            search_btn = find_components(d, "search")
            if search_btn is not None:
                d.click(*coordinate_bounds(search_btn["bounds"]))

            while not d(className="android.widget.EditText").exists():
                time.sleep(0.2)
            d(className="android.widget.EditText").send_keys(order["name"])

            while not d(resourceId="com.grabtaxi.passenger:id/recycler_view").exists():
                time.sleep(0.2)
            # pick 1st element
            recycler = d(resourceId="com.grabtaxi.passenger:id/recycler_view")

            # Then go into the first ComposeView and its children manually
            target = recycler.child(className="androidx.compose.ui.platform.ComposeView", instance=0) \
                            .child(className="android.view.View") \
                            .child(className="android.view.View").click()

            while True:
                if d(resourceId="com.grabtaxi.passenger:id/duxton_icon_button_add").exists():
                    break
                d.swipe(0.5, 0.8, 0.5, 0.5, duration=0.2)
                print("swipe down")
            time.sleep(0.2)
            if order["pref"] == "regular":

                # press add button
                print("add button")
                if order["pcs"] > 1:
                    for i in range(order["pcs"] - 1):
                        print("click add")
                        d(resourceId="com.grabtaxi.passenger:id/duxton_icon_button_add").click()
                        time.sleep(0.2)
                print("confirm button")
                # press confirm button
                while not find_components_by_id(d, "com.grabtaxi.passenger:id/gds_button_content_layout")[0]:
                    time.sleep(0.2)
                    print("wait for confirm button")
                cfm_comp = find_components_by_id(d, "com.grabtaxi.passenger:id/gds_button_content_layout")[0]
                if cfm_comp is not None:
                    d.click(*coordinate_bounds(cfm_comp["bounds"]))
                if idx != len(orders) - 1:
                    time.sleep(0.2)
                    d.press("back")
                else:
            
                    # check out
                    while not find_components_by_id(d, "com.grabtaxi.passenger:id/search_bottom_place_holder"):
                        time.sleep(0.2)
                        print("wait for checkout")
                    checkout_comp = find_components_by_id(d, "com.grabtaxi.passenger:id/search_bottom_place_holder")[0]
                    if checkout_comp is not None:
                        d.click(*coordinate_bounds(checkout_comp["bounds"]))
                    
                    while not d(resourceId="com.grabtaxi.passenger:id/gf_checkout_total").exists():
                        time.sleep(0.2)
                    # check voucher
                    d(scrollable=True).scroll.toEnd()
                    time.sleep(0.4)
                    while not d(description="CODE_OFFER_MESSAGE").exists():
                        time.sleep(0.2)
                    el = d(description="CODE_OFFER_MESSAGE")[0]
                    bounds_raw = el.bounds()
                    bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
                    d.click(*coordinate_bounds(bounds))

                    while not d(resourceId="com.grabtaxi.passenger:id/promo_code_edittext").exists():
                        time.sleep(0.2)
                    el = d(resourceId="com.grabtaxi.passenger:id/compose_view")[1]
                    bounds_raw = el.bounds()
                    bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
                    d.click(*coordinate_bounds(bounds))

                    while not d(resourceId="com.grabtaxi.passenger:id/btn_offer_details").exists():
                        time.sleep(0.2)
                    if d(text="Unavailable").exists():
                        d.press("back")
                        d.press("back")
                    else:
                        d(resourceId="com.grabtaxi.passenger:id/btn_offer_details").click()
                    time.sleep(0.8)
                    # end voucher flow
                    
                    price = d(resourceId="com.grabtaxi.passenger:id/gf_checkout_total").get_text()
                    print(price)
                    return {
                        "status": "success",
                        "price": price,
                        "app": "grab"
                    }
            else :
                # Parse dump
                xml = d.dump_hierarchy()
                root = ET.fromstring(xml)
                special_request = traverse(root)
                specials.append(special_request)
                print(specials)
                d.press("back")
                d.press("back")
        cache_set("food_order", {
                    "restaurant": restaurant,
                    "dropoff": dropoff,
                    "orders": orders,
                    "note": note
                })
        return specials

    except Exception as e:
        print(f"Error occurred: {e}")
        # notify_n8n("1333039921", e)
        return {"message": str(e)}
def confirm_order(specials):
    try:
        order_detail = cache_get("food_order")
        d = u2.connect()
        d.app_start("com.grabtaxi.passenger") 
        for idx, order in enumerate(order_detail["orders"]):
            while not d(resourceId="com.grabtaxi.passenger:id/shortcutComposeContainer").exists():
                print("skrol")
                d.swipe(0.5, 0.7, 0.5, 0.5, duration=0.2)

            search_btn = find_components(d, "search")
            if search_btn is not None:
                d.click(*coordinate_bounds(search_btn["bounds"]))

            while not d(className="android.widget.EditText").exists():
                time.sleep(0.2)
            d(className="android.widget.EditText").send_keys(order["name"])

            while not d(resourceId="com.grabtaxi.passenger:id/recycler_view").exists():
                time.sleep(0.2)
            # pick 1st element
            recycler = d(resourceId="com.grabtaxi.passenger:id/recycler_view")

            # Then go into the first ComposeView and its children manually
            target = recycler.child(className="androidx.compose.ui.platform.ComposeView", instance=0) \
                            .child(className="android.view.View") \
                            .child(className="android.view.View").click()

            while True:
                if d(resourceId="com.grabtaxi.passenger:id/duxton_icon_button_add").exists():
                    break
                d.swipe(0.5, 0.8, 0.5, 0.5, duration=0.2)
                print("swipe down")
            time.sleep(0.2)
            print("specials:", specials[idx])
            for req in specials[idx]:
                chosen = find_components(d, req)
                if chosen is not None:
                    d.click(*coordinate_bounds(chosen["bounds"]))
                    print("click req: ", req)

            if order["pcs"] > 1:
                    for i in range(order["pcs"] - 1):
                        print("click add")
                        d(resourceId="com.grabtaxi.passenger:id/duxton_icon_button_add").click()
                        time.sleep(0.2)
            print("confirm button")
            # press confirm button
            while not find_components_by_id(d, "com.grabtaxi.passenger:id/gds_button_content_layout")[0]:
                time.sleep(0.2)
            time.sleep(0.2)
            while not find_components_by_id(d, "com.grabtaxi.passenger:id/gds_button_content_layout")[0]:
                time.sleep(0.2)
                print("wait for confirm button")
            cfm_comp = find_components_by_id(d, "com.grabtaxi.passenger:id/gds_button_content_layout")[0]
            if cfm_comp is not None:
                d.click(*coordinate_bounds(cfm_comp["bounds"]))
            if idx != len(orders) - 1:
                time.sleep(0.2)
                d.press("back")
            else:
        
                # check out
                while not find_components_by_id(d, "com.grabtaxi.passenger:id/search_bottom_place_holder"):
                    time.sleep(0.2)
                    print("wait for checkout")
                checkout_comp = find_components_by_id(d, "com.grabtaxi.passenger:id/search_bottom_place_holder")[0]
                if checkout_comp is not None:
                    d.click(*coordinate_bounds(checkout_comp["bounds"]))
                
                while not d(resourceId="com.grabtaxi.passenger:id/gf_checkout_total").exists():
                    time.sleep(0.2)

                # check voucher
                d(scrollable=True).scroll.toEnd()
                time.sleep(0.4)
                while not d(description="CODE_OFFER_MESSAGE").exists():
                    time.sleep(0.2)
                el = d(description="CODE_OFFER_MESSAGE")[0]
                bounds_raw = el.bounds()
                bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
                d.click(*coordinate_bounds(bounds))

                while not d(resourceId="com.grabtaxi.passenger:id/promo_code_edittext").exists():
                    time.sleep(0.2)
                el = d(resourceId="com.grabtaxi.passenger:id/compose_view")[1]
                bounds_raw = el.bounds()
                bounds = f"[{bounds_raw[0]},{bounds_raw[1]}][{bounds_raw[2]},{bounds_raw[3]}]"
                d.click(*coordinate_bounds(bounds))

                while not d(resourceId="com.grabtaxi.passenger:id/btn_offer_details").exists():
                    time.sleep(0.2)
                if d(text="Unavailable").exists():
                    d.press("back")
                    d.press("back")
                else:
                    d(resourceId="com.grabtaxi.passenger:id/btn_offer_details").click()
                time.sleep(0.8)
                # end voucher flow
                
                    
                price = d(resourceId="com.grabtaxi.passenger:id/gf_checkout_total").get_text()
                print(price)
                return {
                    "price": price
                }
    
    except Exception as e:
        print("Error occurred:")
        traceback.print_exc()
        return {"message": str(e)}

def checkout(note):
    
    d = u2.connect()
    d.app_start("com.grabtaxi.passenger", stop=False) 

    d(scrollable=True).scroll.toBeginning()
    time.sleep(0.3)
    while not d(text="Delivery options").exists():
        print("swipe")
        d.swipe(0.5, 0.7, 0.5, 0.5, duration=0.05)
    d(text="Add").click()

    d(text="E.g. Leave it at the security post, take service lift, etc.").click()
    d.shell(f"input text '{note}'")
    d(text="Confirm").click()

    while not d(text="Place Order").exists():
        time.sleep(0.2)
    d(text="Place Order").click()


def traverse(node, parent=None, grandparent=None):
    results = []
    desc = node.attrib.get('content-desc', '')

    if desc == 'checkbox_tick':
        parent_sibling_text = None

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
                "request": parent_sibling_text,
            }
        )

    # Traverse children recursively
    for child in node:
        results.extend(traverse(child, node, parent))

    return results
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
    
    # check_order_food(restaurant, dropoff, orders)
    checkout("awkoakwo")
    # special_reqs = [[ "remove pineapple", "remove black pepper mayo" ]]
    # special_reqs = [[ "remove pineapple", "remove black pepper mayo" ], ["remove bigmac sauce", "remove onion"]]
    # confirm_order(special_reqs)
import uiautomator2 as u2
import time
from .utils import check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def check_price(restaurant, dropoff, order, pcs=1, note= ""):
    try:
        d = u2.connect()
        # sess = d.session("com.gojek.app") 
        # d.app_start("com.global.foodpanda.android", stop=True)
        # time.sleep(2)
        d.app_start("com.global.foodpanda.android", stop=False)
        # time.sleep(2)
        # accept_permissions(d)
        # clear_unexpected_popups(d)
        # screen_components(d)
        # # Call login checker
        # if not check_login_status(d):
        #     raise Exception("User is not logged in. Please log in to continue.")
        
        # while not d(resourceId="HomeSearchBar").exists():
        #     time.sleep(0.1)
        # d(resourceId="HomeSearchBar").click()

        # search = d(className="android.widget.EditText")[0]
        # search.send_keys(restaurant)

        # time.sleep(0.3)

        # # pick in restaurant
        # restaurant_comp = find_components(d, "in restaurants")
        # if restaurant_comp is not None:
        #     d.click(*coordinate_bounds(restaurant_comp["bounds"]))
        
        # while not d(resourceId="LARGE_TITLE").exists():
        #     time.sleep(0.1)
        # d(resourceId="LARGE_TITLE").click()

        # while not d(resourceId="search_bar").exists():
        #     time.sleep(0.1)
        # d(resourceId="search_bar").click()

        # while not d(resourceId="com.global.foodpanda.android:id/searchEditText").exists():
        #     time.sleep(0.1)
        # d(resourceId="com.global.foodpanda.android:id/searchEditText").send_keys(order)

        while not d(resourceId="com.global.foodpanda.android:id/titleTextView").exists():
            time.sleep(0.1)
        # # d.hide_keyboard()
        d(resourceId="com.global.foodpanda.android:id/dishTileLayout").click()
        # # we can display the list then ask user
        # get all the menu
        return 
       
    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
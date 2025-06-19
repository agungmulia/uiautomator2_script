import uiautomator2 as u2
import time
from utils import select_language, check_login_status, clear_unexpected_popups, accept_permissions, screen_components, find_components, find_components_by_id, coordinate_bounds
def check_price(destination, pickup_time):
    try:
        print("init check price")
        d = u2.connect()
        d.app_start("com.codigo.comfort", stop=False)
        time.sleep(2)
        clear_unexpected_popups(d)
        # select language
        accept_permissions(d)

        select_language(d)

        if not check_login_status(d):
            print("User is not logged in. Please log in to continue.")
            return 
        # d.app_start("com.gojek.app", stop=False)
        # accept_permissions(d)
        # clear_unexpected_popups(d)

        # # Call login checker
        # if not check_login_status(d):
        #     raise Exception("User is not logged in. Please log in to continue.")
        # clear_unexpected_popups(d)

        # # Continue automation like booking ride
        # print("📲 Proceeding to book ride...")
        




    except Exception as e:
        # d = u2.connect()
        # sess = d.session("org.telegram.messenger") 
        # notify_n8n("1333039921", e)
        print(f"[Error] Failed to book ride: {e}")
        return
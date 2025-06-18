# cli_runner.py

import sys
from .services.book_ride import book_ride_handler
from .services.order_food import order_food_handler
from .services.confirmation_check import confirmation_check_handler

if __name__ == "__main__":
    try:
        action = sys.argv[1]
        if action == "check_price":
            destination = sys.argv[2]
            time = sys.argv[3]
            result = confirmation_check_handler(destination, time)
        if action == "book_ride":
            destination = sys.argv[2]
            time = sys.argv[3]
            result = book_ride_handler(destination, time)
        elif action == "order_food":
            item = sys.argv[2]
            quantity = sys.argv[3]
            result = order_food_handler(item, quantity)

        else:
            raise ValueError("Unknown action")

        print(result)

    except IndexError:
        print("Usage:")
        print("  python cli_runner.py book_ride <destination> <time>")
        print("  python cli_runner.py order_food <item> <quantity>")
    except Exception as e:
        print(f"Error: {e}")

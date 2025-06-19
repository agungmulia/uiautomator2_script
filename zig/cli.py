import sys
# from book_ride import book_ride
from check_price import check_price
# from cancel_ride import cancel_ride
if __name__ == "__main__":
    try:
        action = sys.argv[1]

        # if action == "book_ride":
        #     destination = sys.argv[2]
        #     time = sys.argv[3]
        #     result = book_ride(destination, time)
        if action == "check_price":
            destination = sys.argv[2]
            time = sys.argv[3]
            result = check_price(destination, time)
        # elif action == "cancel_ride":
        #     destination = sys.argv[2]
        #     time = sys.argv[3]
        #     result = cancel_ride()

        # elif action == "order_food":
        #     item = sys.argv[2]
        #     quantity = sys.argv[3]
        #     result = order_food(item, quantity)

        else:
            raise ValueError("Unknown action")

        print(result)

    except IndexError:
        print("Usage:")
        print("  python cli_runner.py book_ride <destination> <time>")
        print("  python cli_runner.py order_food <item> <quantity>")
    except Exception as e:
        print(f"Error: {e}")

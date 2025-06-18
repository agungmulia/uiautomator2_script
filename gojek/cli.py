import sys
from book_ride import book_ride
if __name__ == "__main__":
    try:
        action = sys.argv[1]

        if action == "book_ride":
            destination = sys.argv[2]
            time = sys.argv[3]
            result = book_ride(destination, time)

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

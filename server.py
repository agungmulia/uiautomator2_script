from flask import Flask, request, jsonify
from Grab.services import book_ride_handler, order_food_handler, confirmation_check_handler
from ryde.service.check_price import check_price as ryde_check_price
from ryde.service.book_ride import book_ride as ryde_book_ride
from foodpanda.check_price import check_price as foodpanda_check_price
from gojek.check_price import check_price as gojek_check_price
from gojek.book_ride import book_ride as gojek_book_ride
from gojek.cancel_ride import cancel_ride as gojek_cancel_ride
from zig.check_price import check_price as zig_check_price
from zig.cancel_ride import cancel_ride as zig_cancel_ride
from zig.book_ride import book_ride as zig_book_ride
import time
app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return "API is running", 200

@app.route("/grab", methods=["POST"])
def grab():
    try:
        print("Received request:", request.json)
        print("book_ride is:", book_ride_handler)
        data = request.get_json()
        action = data.get("action")
        args = data.get("args", {})

        if action == "book_ride":
            booking_option = data.get("booking_option")
            result = book_ride_handler(booking_option)

        elif action == "order_food":
            result = order_food_handler(args.get("item"), args.get("quantity"))

        elif action == "confirmation_check":
            result = confirmation_check_handler(data.get("destination"), data.get("time"))
        # elif action == "cancel_ride":
        #     result = confirmation_check_handler(data.get("destination"), data.get("time"))

        else:
            return jsonify({"error": "Unknown action"}), 400

        print("Result:", result)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/gojek", methods=["POST"])
def gojek():
    try:
        print("Received request:", request.json)
        data = request.get_json()
        action = data.get("action")
        args = data.get("args", {})

        if action == "book_ride":
            ride = data.get("booking_option")
            result = gojek_book_ride(ride)

        # elif action == "order_food":
        #     result = gojek(args.get("item"), args.get("quantity"))

        elif action == "confirmation_check":
            result = gojek_check_price(data.get("destination"), data.get("time"))
        elif action == "cancel_ride":
            result = gojek_cancel_ride()

        else:
            return jsonify({"error": "Unknown action"}), 400

        print("Result:", result)

        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/zig", methods=["POST"])
def zig():
    try:
        print("Received request:", request.json)
        data = request.get_json()
        action = data.get("action")
        args = data.get("args", {})

        if action == "book_ride":
            booking_option = data.get("booking_option")
            result = zig_book_ride(booking_option)

        # elif action == "order_food":
        #     result = gojek(args.get("item"), args.get("quantity"))

        elif action == "confirmation_check":
            result = zig_check_price(data.get("destination"), data.get("time"))
        elif action == "cancel_ride":
            result = zig_cancel_ride(data.get("destination"), data.get("time"))

        else:
            return jsonify({"error": "Unknown action"}), 400

        print("Result:", result)

        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/ryde", methods=["POST"])
def ryde():
    try:
        print("Received request:", request.json)
        data = request.get_json()
        action = data.get("action")
        args = data.get("args", {})

        if action == "book_ride":
            booking_option = data.get("booking_option")
            result = ryde_book_ride(booking_option)

        # elif action == "order_food":
        #     result = gojek(args.get("item"), args.get("quantity"))

        if action == "confirmation_check":
            result = ryde_check_price(data.get("destination"), data.get("time"))
        # elif action == "cancel_ride":
        #     result = zig_cancel_ride(data.get("destination"), data.get("time"))

        else:
            return jsonify({"error": "Unknown action"}), 400

        print("Result:", result)

        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/foodpanda", methods=["POST"])
def foodpanda():
    try:
        print("Received request:", request.json)
        data = request.get_json()
        action = data.get("action")
        args = data.get("args", {})

        # if action == "order_food":
        #     booking_option = data.get("booking_option")
        #     result = ryde_book_ride(booking_option)

        if action == "confirmation_check":
            print(data)
            result = foodpanda_check_price(data.get("restaurant"), data.get("dropoff"), data.get("order"))
        # elif action == "cancel_ride":
        #     result = zig_cancel_ride(data.get("destination"), data.get("time"))

        else:
            return jsonify({"error": "Unknown action"}), 400

        print("Result:", result)

        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/all_transport_app", methods=["POST"])
def all_transport_app():
    try:
        time_start = time.time()
        print("Received request:", request.json)
        print("book_ride is:", book_ride_handler)
        data = request.get_json()
        action = data.get("action")
        args = data.get("args", {})

        result = []
        if action == "confirmation_check":
            ryde_result = ryde_check_price(data.get("destination"), data.get("time"))
            grab_result = confirmation_check_handler(data.get("destination"), data.get("time"))
            gojek_result = gojek_check_price(data.get("destination"), data.get("time"))
            zig_result = zig_check_price(data.get("destination"), data.get("time"))
            result = {
                "grab": grab_result,
                "gojek": gojek_result,
                "zig": zig_result,
                "ryde": ryde_result
            }
        else:
            return jsonify({"error": "Unknown action"}), 400

        print("Result:", result)
        end_time = time.time()
        print(f"Execution time: {end_time - time_start:.4f} seconds")
        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
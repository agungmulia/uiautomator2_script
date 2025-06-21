from flask import Flask, request, jsonify
from Grab.services import book_ride_handler, order_food_handler, confirmation_check_handler
from gojek.check_price import check_price as gojek_check_price
from gojek.book_ride import book_ride as gojek_book_ride

from zig.check_price import check_price as zig_check_price
from zig.book_ride import book_ride as zig_book_ride
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
            result = book_ride_handler(data.get("destination"), data.get("time"))

        elif action == "order_food":
            result = order_food_handler(args.get("item"), args.get("quantity"))

        elif action == "confirmation_check":
            result = confirmation_check_handler(data.get("destination"), data.get("time"))

        else:
            return jsonify({"error": "Unknown action"}), 400

        print("Result:", result)

        return jsonify({"message": result})
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
            result = gojek_book_ride(data.get("destination"), data.get("time"))

        # elif action == "order_food":
        #     result = gojek(args.get("item"), args.get("quantity"))

        elif action == "confirmation_check":
            result = gojek_check_price(data.get("destination"), data.get("time"))

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
            result = zig_book_ride(data.get("destination"), data.get("time"))

        # elif action == "order_food":
        #     result = gojek(args.get("item"), args.get("quantity"))

        elif action == "confirmation_check":
            result = zig_check_price(data.get("destination"), data.get("time"))

        else:
            return jsonify({"error": "Unknown action"}), 400

        print("Result:", result)

        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/all_transport_app", methods=["POST"])
def all_transport_app():
    try:
        print("Received request:", request.json)
        print("book_ride is:", book_ride_handler)
        data = request.get_json()
        action = data.get("action")
        args = data.get("args", {})

        result = []
        if action == "confirmation_check":
            grab_result = confirmation_check_handler(data.get("destination"), data.get("time"))
            gojek_result = gojek_check_price(data.get("destination"), data.get("time"))
            zig_result = zig_check_price(data.get("destination"), data.get("time"))
            result = [grab_result, gojek_result, zig_result]
        else:
            return jsonify({"error": "Unknown action"}), 400

        print("Result:", result)

        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
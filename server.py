from flask import Flask, request, jsonify
from Grab.services import book_ride_handler, order_food_handler, confirmation_check_handler

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
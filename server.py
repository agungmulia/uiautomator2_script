from flask import Flask, request, jsonify
from Grab.services import book_ride, order_food

app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return "API is running", 200

@app.route("/grab", methods=["POST"])
def grab():
    try:
        data = request.get_json()
        action = data.get("action")
        args = data.get("args", {})

        if action == "book_ride":
            result = book_ride(args.get("destination"), args.get("time"))

        elif action == "order_food":
            result = order_food(args.get("item"), args.get("quantity"))

        else:
            return jsonify({"error": "Unknown action"}), 400

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify
from Grab.services import book_ride_handler, order_food_handler, confirmation_check_handler
from gojek.check_price import check_price as gojek_check_price
from gojek.book_ride import book_ride as gojek_book_ride
from zig.check_price import check_price as zig_check_price
from zig.book_ride import book_ride as zig_book_ride
from data import FlowState, TransportBookingData, parse_booking_options, parse_selected_option, BookingOption, SelectedOption, BookingResult, parse_booking_result
import time
from dataclasses import asdict
import random
app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return "API is running", 200

@app.route("/transport/flow", methods=["POST"])
def transport_flow():
    req = request.get_json()

    flow = req.get("flow")
    step = req.get("step")
    raw_data = req.get("data", {})

    data = TransportBookingData(
        pickup_location=raw_data.get("pickup_location"),
        destination=raw_data.get("destination"),
        time=raw_data.get("time", "now"),
        app=raw_data.get("app"),
        payment_method=raw_data.get("payment_method"),
        confirmation_check_done=raw_data.get("confirmation_check_done", False),
        booking_options=parse_booking_options(raw_data.get("booking_options", [])),
        selected_option=parse_selected_option(raw_data.get("selected_option")),
        booking_result=parse_booking_result(raw_data.get("booking_result")),
        cancelled=raw_data.get("cancelled", False)
    )

    state = FlowState(flow="transport_booking", step=step, data=data)

    # FSM Logic
    if state.step == "awaiting_missing_info":
        if state.data.destination:
            state.step = "confirmation_check_pending"

    elif state.step == "confirmation_check_pending":
        state.data.booking_options = [
            BookingOption(title="JustGrab", app="grab", price=50000, option_id="justgrab-grab-001"),
            BookingOption(title="GoCar", app="gojek", price=48000, option_id="gocar-gojek-002")
        ]
        state.data.confirmation_check_done = True
        state.step = "awaiting_user_confirmation"

    elif state.step == "awaiting_user_confirmation":
        if state.data.selected_option:
            if not state.data.payment_method:
                state.step = "ask_payment_method"
            else:
                state.step = "booking_in_progress"

    elif state.step == "ask_payment_method":
        if state.data.payment_method:
            state.step = "booking_in_progress"

    elif state.step == "booking_in_progress":
        waiting_time = random.randint(5, 15)
        state.data.booking_result = BookingResult(status="success", waiting_time=waiting_time)
        state.step = "handle_waiting_time"

    elif state.step == "handle_waiting_time":
        if state.data.booking_result and state.data.booking_result.waiting_time > 10:
            state.step = "cancel_and_restart"
        else:
            state.step = "done"

    elif state.step == "cancel_and_restart":
        state.data.selected_option = None
        state.data.booking_result = None
        state.data.confirmation_check_done = False
        state.step = "confirmation_check_pending"

    return jsonify(asdict(state))
    
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
            # result = book_ride_handler(booking_option)

        elif action == "order_food":
            result = order_food_handler(args.get("item"), args.get("quantity"))

        elif action == "confirmation_check":
            result = confirmation_check_handler(data.get("destination"), data.get("time"))

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
            # result = gojek_book_ride(ride)
            result = {"ride": ride, "waiting_time": "11 mins", "status": "success"}

        # elif action == "order_food":
        #     result = gojek(args.get("item"), args.get("quantity"))

        elif action == "confirmation_check":
            result = gojek_check_price(data.get("destination"), data.get("time"))
        elif action == "cancel_ride":
            # result = gojek_check_price(data.get("destination"), data.get("time"))
            result = {"status": "success", "message": "Ride cancelled"}

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
            # result = zig_book_ride(booking_option)
            
            result = {"ride": booking_option, "waiting_time": "11 mins", "status": "success"}

        # elif action == "order_food":
        #     result = gojek(args.get("item"), args.get("quantity"))

        elif action == "confirmation_check":
            result = zig_check_price(data.get("destination"), data.get("time"))
        elif action == "cancel_ride":
            # result = zig_check_price(data.get("destination"), data.get("time"))
            result = {"status": "success", "message": "Ride cancelled"}

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
            # grab_result = confirmation_check_handler(data.get("destination"), data.get("time"))
            # gojek_result = gojek_check_price(data.get("destination"), data.get("time"))
            # zig_result = zig_check_price(data.get("destination"), data.get("time"))
            # result = {
            #     "grab": grab_result,
            #     "gojek": gojek_result,
            #     "zig": zig_result
            # }
            result = {
                "grab": [{
                        "title": "premium | 6 seats",
                        "price": "$15.00",
                    }],
                "gojek": [{
                        "title": "gocar",
                        "price": "$11.00",
                    }],
                "zig": [{
                        "title": "Taxi or car (flat fare)",
                        "price": "$12.00",
                    }],

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
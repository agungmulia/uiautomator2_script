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
from tada.check_price import check_price as tada_check_price
from tada.book_ride import book_ride as tada_book_ride
from tada.cancel_ride import cancel_ride as tada_cancel_ride

import time
from data import FlowState, TransportBookingData, parse_booking_options, parse_selected_option, BookingOption, SelectedOption, BookingResult, parse_booking_result, fetch_rides
import time
from dataclasses import asdict

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

@app.route("/transport/flow", methods=["POST"])
def transport_flow():
    req = request.get_json()

    flow = req.get("flow")
    step = req.get("step")
    raw_data = req.get("data", {})
    print("step:", step, "raw data:", raw_data)
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
        booking_options = []
        
        if state.data.app is None:
            tada_result = tada_check_price(state.data.destination, state.data.time)
            if tada_result is not None:
                for i, opt in enumerate(tada_result):
                    booking_options.append(
                    BookingOption(
                        title=opt["title"],
                        app="tada",
                        price=opt["price"],
                        option_id=f"{opt['title'].lower().replace(' ', '')}-tada-{i:03}"
                    )
                )
                    
            ryde_result = ryde_check_price(state.data.destination, state.data.time)
            if ryde_result is not None:
                for i, opt in enumerate(ryde_result):
                    booking_options.append(
                    BookingOption(
                        title=opt["title"],
                        app="ryde",
                        price=opt["price"],
                        option_id=f"{opt['title'].lower().replace(' ', '')}-ryde-{i:03}"
                    )
                )
            grab_result = confirmation_check_handler(state.data.destination, state.data.time)
            if grab_result is not None:
                for i, opt in enumerate(grab_result):
                    booking_options.append(
                        BookingOption(
                            title=opt["title"],
                            app="grab",
                            price=opt["price"],
                            option_id=f"{opt['title'].lower().replace(' ', '')}-grab-{i:03}"
                        )
                    )
            gojek_result = gojek_check_price(state.data.destination, state.data.time)
            if gojek_result is not None:
                for i, opt in enumerate(gojek_result):
                    booking_options.append(
                    BookingOption(
                        title=opt["title"],
                        app="gojek",
                        price=opt["price"],
                        option_id=f"{opt['title'].lower().replace(' ', '')}-gojek-{i:03}"
                    )
                )
            zig_result = zig_check_price(state.data.destination, state.data.time)
            if zig_result is not None :
                for i, opt in enumerate(zig_result):
                    booking_options.append(
                    BookingOption(
                        title=opt["title"],
                        app="zig",
                        price=opt["price"],
                        option_id=f"{opt['title'].lower().replace(' ', '')}-zig-{i:03}"
                    )
                )
            
        state.data.booking_options = booking_options
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
        res = None
        if state.data.app.lower() == "grab":
            res = book_ride_handler(state.data.selected_option.title) 
        elif state.data.app.lower() == "ryde":
            res = ryde_book_ride(state.data.selected_option.title)
        elif state.data.app.lower() == "gojek":
            res = gojek_book_ride(state.data.selected_option.title)
        elif state.data.app.lower() == "zig":
            res = zig_book_ride(state.data.selected_option.title)
        elif state.data.app.lower() == "tada":
            res = tada_book_ride(state.data.selected_option.title)
        state.data.booking_result = BookingResult(status=res["status"], waiting_time=res["waiting_time"])
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

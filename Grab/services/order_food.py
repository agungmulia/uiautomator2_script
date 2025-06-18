def order_food_handler(item, quantity):
    return {
        "status": "success",
        "message": f"{quantity}x {item} ordered!"
    }
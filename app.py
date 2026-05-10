from flask import Flask, render_template, request, jsonify, session
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = "icecream-secret-2024"

# In-memory store for orders
orders = {}

MENU = [
    {"id": 1, "name": "Mango Madness", "emoji": "🥭", "price": 120, "desc": "Alphonso mango swirl with cardamom", "color": "#FF9D00"},
    {"id": 2, "name": "Dark Chocolate Dream", "emoji": "🍫", "price": 140, "desc": "Belgian dark chocolate with sea salt", "color": "#3D1A00"},
    {"id": 3, "name": "Strawberry Fields", "emoji": "🍓", "price": 110, "desc": "Fresh strawberry with basil ripple", "color": "#FF4B6E"},
    {"id": 4, "name": "Pistachio Royal", "emoji": "🫘", "price": 160, "desc": "Iranian pistachio with rose water", "color": "#7CB87C"},
    {"id": 5, "name": "Coconut Bliss", "emoji": "🥥", "price": 130, "desc": "Tender coconut with saffron threads", "color": "#F5DEB3"},
    {"id": 6, "name": "Butter Scotch", "emoji": "🍯", "price": 115, "desc": "Caramel butterscotch with toffee bits", "color": "#DAA520"},
    {"id": 7, "name": "Blueberry Cheesecake", "emoji": "🫐", "price": 150, "desc": "Wild blueberry on creamy cheesecake base", "color": "#6A5ACD"},
    {"id": 8, "name": "Mint Chocolate Chip", "emoji": "🌿", "price": 125, "desc": "Fresh mint with dark chocolate chips", "color": "#3EB489"},
]

SIZES = [
    {"id": "single", "label": "Single Scoop", "multiplier": 1.0, "emoji": "🍦"},
    {"id": "double", "label": "Double Scoop", "multiplier": 1.7, "emoji": "🍧"},
    {"id": "triple", "label": "Triple Scoop", "multiplier": 2.3, "emoji": "🎉"},
]

TOPPINGS = [
    {"id": "sprinkles", "name": "Rainbow Sprinkles", "price": 15, "emoji": "🌈"},
    {"id": "wafer", "name": "Wafer Cone", "price": 20, "emoji": "🥞"},
    {"id": "nuts", "name": "Roasted Nuts", "price": 25, "emoji": "🥜"},
    {"id": "syrup", "name": "Chocolate Syrup", "price": 20, "emoji": "🍫"},
    {"id": "cherry", "name": "Maraschino Cherry", "price": 10, "emoji": "🍒"},
]

@app.route("/")
def index():
    return render_template("index.html", menu=MENU, sizes=SIZES, toppings=TOPPINGS)

@app.route("/api/order", methods=["POST"])
def place_order():
    data = request.json
    order_id = str(uuid.uuid4())[:8].upper()
    
    flavor = next((f for f in MENU if f["id"] == data.get("flavor_id")), None)
    size = next((s for s in SIZES if s["id"] == data.get("size_id")), None)
    selected_toppings = [t for t in TOPPINGS if t["id"] in data.get("toppings", [])]
    
    if not flavor or not size:
        return jsonify({"error": "Invalid selection"}), 400
    
    base_price = flavor["price"] * size["multiplier"]
    topping_price = sum(t["price"] for t in selected_toppings)
    total = round(base_price + topping_price)
    
    order = {
        "id": order_id,
        "flavor": flavor["name"],
        "flavor_emoji": flavor["emoji"],
        "size": size["label"],
        "toppings": [t["name"] for t in selected_toppings],
        "total": total,
        "name": data.get("name", "Friend"),
        "timestamp": datetime.now().strftime("%I:%M %p"),
        "status": "confirmed"
    }
    orders[order_id] = order
    
    return jsonify({"success": True, "order": order})

@app.route("/api/orders")
def get_orders():
    return jsonify(list(orders.values())[-10:])

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5050)

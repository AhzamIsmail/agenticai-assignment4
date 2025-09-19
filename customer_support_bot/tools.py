# # customer_support_bot/tools.py
from .sdk import function_tool
from .config import ORDERS

def is_enabled(query: str, metadata: dict) -> bool:
    return "order" in query.lower() or "status" in query.lower()

def error_function(error_message: str, kwargs: dict):
    order_id = kwargs.get("order_id")
    return {"error": f"Order {order_id} not found", "message": "Please provide a valid order ID."}

@function_tool("get_order_status", is_enabled=is_enabled, error_function=error_function)
def get_order_status(order_id: str, customer_id: str = None):
    if order_id not in ORDERS:
        raise KeyError("Order not found")
    return ORDERS[order_id]



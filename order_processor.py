import json
import logging
from logging.handlers import RotatingFileHandler


logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = RotatingFileHandler("log.txt", maxBytes=1024 * 1024, backupCount=3)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


TAX_RATE = 0.18
SHIPPING_THRESHOLD = 1000
SHIPPING_FEE = 50
DISCOUNT_THRESHOLD = 500
DISCOUNT_RATE = 0.9


def process_order(order):
    if not isinstance(order, (list, tuple)):
        raise TypeError("order must be a list or tuple of item dictionaries")

    total = 0
    for item in order:
        if not isinstance(item, dict):
            raise TypeError("each order item must be a dictionary")
        if 'price' not in item or 'quantity' not in item or 'name' not in item:
            raise KeyError("each order item must contain 'price', 'quantity', and 'name'")
        total += item['price'] * item['quantity']

    tax = total * TAX_RATE
    total_with_tax = total + tax

    # formatting
    print("Order Summary")
    for item in order:
        print(item['name'], item['quantity'], item['price'])

    logger.info("Order Summary: %s", json.dumps(order, default=str, ensure_ascii=True))

    # shipping logic
    if total > SHIPPING_THRESHOLD:
        shipping = 0
    else:
        shipping = SHIPPING_FEE

    total_with_tax += shipping

    # discount logic
    if total > DISCOUNT_THRESHOLD:
        total_with_tax *= DISCOUNT_RATE

    print("Final Total:", total_with_tax)

    return total_with_tax
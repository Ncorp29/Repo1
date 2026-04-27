TAX_RATE = 0.18
FREE_SHIPPING_THRESHOLD = 1000
SHIPPING_COST = 50
DISCOUNT_THRESHOLD = 500
DISCOUNT_MULTIPLIER = 0.9


def calculate_subtotal(order):
    total = 0
    for item in order:
        try:
            price = item.get('price', 0)
            quantity = item.get('quantity', 0)
            total += float(price) * float(quantity)
        except (AttributeError, TypeError, ValueError):
            continue
    return total


def calculate_tax(total):
    return total * TAX_RATE


def calculate_shipping(total):
    if total > FREE_SHIPPING_THRESHOLD:
        return 0
    return SHIPPING_COST


def calculate_discount(total):
    if total > DISCOUNT_THRESHOLD:
        return DISCOUNT_MULTIPLIER
    return 1.0


def format_order_summary(order, total_with_tax):
    lines = ["Order Summary"]
    for item in order:
        try:
            name = item.get('name', 'Unknown')
            quantity = item.get('quantity', 0)
            price = item.get('price', 0)
        except AttributeError:
            name = 'Unknown'
            quantity = 0
            price = 0
        lines.append(f"{name} {quantity} {price}")
    lines.append(f"Final Total: {total_with_tax}")
    return lines


def process_order(order):
    total = 0
    lines = ["Order Summary"]

    for item in order:
        try:
            price = item.get('price', 0)
            quantity = item.get('quantity', 0)
            name = item.get('name', 'Unknown')
        except AttributeError:
            price = 0
            quantity = 0
            name = 'Unknown'

        try:
            total += float(price) * float(quantity)
        except (TypeError, ValueError):
            pass

        lines.append(f"{name} {quantity} {price}")

    tax = calculate_tax(total)
    total_with_tax = total + tax

    # formatting
    lines.append(f"Final Total: {total_with_tax}")
    for line in lines:
        print(line)

    # shipping logic
    shipping = calculate_shipping(total)

    total_with_tax += shipping

    # discount logic
    discount_multiplier = calculate_discount(total)
    total_with_tax *= discount_multiplier

    with open("log.txt", "a") as f:
        f.write(str(order))

    return total_with_tax
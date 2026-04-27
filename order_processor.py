def process_order(order):
    total = 0
    for item in order:
        total += item['price'] * item['quantity']

    tax = total * 0.18
    total_with_tax = total + tax

    # formatting
    print("Order Summary")
    for item in order:
        print(item['name'], item['quantity'], item['price'])

    # shipping logic
    if total > 1000:
        shipping = 0
    else:
        shipping = 50

    total_with_tax += shipping

    # discount logic
    if total > 500:
        total_with_tax *= 0.9

    print("Final Total:", total_with_tax)

    with open("log.txt", "a") as f:
        f.write(str(order))

    return total_with_tax

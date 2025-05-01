from selenium.webdriver.common.devtools.v133.fetch import continue_request

grocery_list = [
    {"item": "apples", "price": 2.00, "quantity": 5, "category": "Produce"},
    {"item": "bread", "price": 3.50, "quantity": 2, "category": "Bakery"},
    {"item": "milk", "price": 4.25, "quantity": 1, "category": "Dairy"},
    {"item": "cheese", "price": 10.00, "quantity": 3, "category": "Dairy"},
    {"item": "gronola", "price": 7.00, "quantity": 3, "category": "Snacks"},
    {"item": "popcorn", "price": 2.00, "quantity": 5, "category": "Snacks"},
]

coupons = {
    "SAVE5": {"type": "order-level", "amount_off": 5, "flag": "$5 OFF SUBTOTAL",},
    "SAVE10": {"type": "order-level", "amount_off": 10, "flag": "$10 OFF SUBTOTAL",},
    "BOGO": {"type": "item-level", "discount": 0.5, "items": ["apples", "soap"], "flag": "BOGO",},
    "FREESHIP": {"type": "shipping", "discount": 0.0, "flag": "FREE SHIPPING",},
    "50OFFSHIP": {"type": "shipping", "discount": 0.50, "flag": "50% OFF SHIPPING",}
}

def generate_sorted_receipt(grocery_list):
    grouped_items = {}
    subtotal = 0

    for item in grocery_list:
        category = item['category']

        if category not in grouped_items:
            grouped_items[category] = []
        grouped_items[category].append(item)

    for category, items in grouped_items.items():
        for item in items:
            item_total = item['quantity'] * item['price']
            subtotal += item_total

    return grouped_items, subtotal

def apply_shipping(distance):
    cost_per_mile = 0.05
    shipping_cost = cost_per_mile * int(distance)
    return shipping_cost

def apply_coupon(grocery_list, coupon_code=None):
    grouped_items, subtotal = generate_sorted_receipt(grocery_list)

    flag = None
    coupon_valid = False
    shipping_discount = 1.0

    if coupon_code:
        for code, data in coupons.items():
            if code == coupon_code:
                flag = data['flag']
                coupon_valid = True

                if data['type'] == 'order-level':
                    subtotal -= data['amount_off']

                if data['type'] == 'item-level':
                    for category_items in grouped_items.values():
                        for product in category_items:
                            if product['item'] in data['items']:
                                product['price'] *= data['discount']

                if data['type'] == "shipping":
                    shipping_discount = data['discount']

                break
    return grouped_items, subtotal, flag, coupon_valid, shipping_discount


def main_checkout():
    tax = 0.0525

    #call function
    grouped_items, subtotal, flag, coupon_valid, shipping_discount = apply_coupon(grocery_list, coupon_code)

    total_with_tax = subtotal + (subtotal * tax)
    discounted_shipping = shipping_cost * shipping_discount
    grand_total = total_with_tax + discounted_shipping

    receipt_lines = []

    receipt_lines.append("Items purchased:")
    receipt_lines.append("=" * 20)

    #item list
    for category, data in grouped_items.items():
        receipt_lines.append(f"\nCategory: {category}")
        for items in data:
            receipt_lines.append(f"- {items['item']} {items['quantity']} @ ${items['price']:.2f}")

    receipt_lines.append("=" * 20)
    #price calculations
    if coupon_valid:
        receipt_lines.append(f"*****{flag}*****")
    receipt_lines.append(f"Subtotal: ${subtotal:.2f}")
    receipt_lines.append(f"Tax {tax * 100}%: +${subtotal * tax:.2f}")
    receipt_lines.append(f"Total with tax: = ${total_with_tax:.2f}")
    receipt_lines.append(f"Shipping: +${shipping_cost:.2f}")
    if shipping_discount < 1.0:
        receipt_lines.append(f"- ${shipping_cost - discounted_shipping:.2f} OFF SHIPPING")

    receipt_lines.append(f"Grand Total: == ${grand_total:.2f}")

    for line in receipt_lines:
        print(line)

# ***** main event loop: *****
coupon_code = input("Enter a coupon code, or press 'enter': ").upper()
if coupon_code.isalpha():
    if coupon_code not in coupons:
        print(f"Sorry, {coupon_code} is not valid at this time.")

shipping_choice = input("Do you need shipping? Y/N: ").upper()
if shipping_choice == "Y":
    shipping_distance = input("Enter how many miles to ship: ")
    shipping_cost = apply_shipping(shipping_distance)
elif shipping_choice == "N":
    shipping_cost = 0



main_checkout()
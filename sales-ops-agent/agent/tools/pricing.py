from agent.tools.inventory import check_inventory

DISCOUNT_TIERS = {
    "bronze": 0,
    "silver": 0.05,
    "gold": 0.10,
    "platinum": 0.15
}


def calculate_quote(items, discount_tier):

    subtotal=0
    line_items=[]

    for item in items:
        inventory=check_inventory(item["sku"])

        if not inventory["found"]:
            return {
                "success": False,
                "error":
                    f"SKU not found: {item['sku']}"
            }

        product=inventory["product"]

        quantity=item["quantity"]

        line_total= product["unit_price"]*quantity

        subtotal+=line_total

        line_items.append(
            {
                "sku": product["sku"],
                "name": product["name"],
                "quantity": quantity,
                "unit_price": product["unit_price"],
                "line_total": line_total
            }
        )

        discount_rate=DISCOUNT_TIERS.get(discount_tier.lower(),0)

        discount_amount = (
            subtotal * discount_rate
        )

        final_total = (
            subtotal - discount_amount
        )

        return {
            "discount_tier": discount_tier,
            "subtotal": subtotal,
            "discount": discount_amount,
            "final_total": final_total,
            "items": line_items
        }
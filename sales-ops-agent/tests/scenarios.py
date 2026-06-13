SCENARIOS = [

    {
        "name":
            "CRM Lookup",

        "prompt":
            "Tell me about priya@example.com",

        "expected_tools":
            ["crm_lookup"]
    },

    {
        "name":
            "Inventory Check",

        "prompt":
            "Do we have LAPTOP001 in stock?",

        "expected_tools":
            ["check_inventory"]
    },

    {
        "name":
            "Bulk Pricing",

        "prompt":
            "Need laptop pricing for 20 units",

        "expected_tools":
            [
                "find_product",
                "calculate_quote"
            ]
    },

    {
        "name":
            "Follow Up Workflow",

        "prompt":
            "Help me follow up with priya@example.com about laptop bulk pricing",

        "expected_tools":
            [
                "crm_lookup",
                "find_product",
                "check_inventory",
                "calculate_quote",
                "draft_email"
            ]
    }
]
from openai.types.chat import ChatCompletionToolParam

TOOLS : list[ChatCompletionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "crm_lookup",
            "description": (
                "Look up lead information in the CRM. "
                "Use when the user references a lead email "
                "or asks about previous customer interactions."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string"
                    }
                },
                "required": ["email"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "check_inventory",
            "description": (
                "Check product inventory using SKU. "
                "Use when product availability is needed."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "sku": {
                        "type": "string"
                    }
                },
                "required": ["sku"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculate_quote",
            "description": (
                "Calculate a quote for products "
                "with discount tiers."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array"
                    },
                    "discount_tier": {
                        "type": "string"
                    }
                },
                "required": [
                    "items",
                    "discount_tier"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "draft_email",
            "description": (
                "Draft a sales email. "
                "Never sends email."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient_name": {
                        "type": "string"
                    },
                    "recipient_email": {
                        "type": "string"
                    },
                    "company": {
                        "type": "string"
                    },
                    "context": {
                        "type": "string"
                    }
                },
                "required": [
                    "recipient_name",
                    "company",
                    "context"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search the web for current information. "
                "Use when external information is needed."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_inventory",
            "description": (
                "List all available inventory products. "
                "Use when the user mentions a product category "
                "such as laptops, monitors, keyboards, or asks "
                "for pricing without providing a SKU."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"find_product",
            "description":
                "Find products by name or keyword. "
                "Use when the user describes a product "
                "without providing a SKU.",
            "parameters":{
                "type":"object",
                "properties":{
                    "keyword":{
                        "type":"string"
                    }
                },
                "required":["keyword"]
            }
        }
    }
]
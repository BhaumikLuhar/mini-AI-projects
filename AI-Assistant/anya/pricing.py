MODEL_PRICING = {
    "development": {
        "input": 0.0,
        "output": 0.0
    },

    "production": {
        "input": 3.0,
        "output": 15.0
    }
}

USD_TO_INR = 83

def calculate_cost(input_tokens, output_tokens, mode="development"):

    pricing=MODEL_PRICING[mode]

    input_cost=input_tokens/1_000_000 * pricing["input"]
    output_cost=output_tokens/1_000_000 * pricing["output"]

    return input_cost+output_cost

def usd_to_inr(amount):
    return amount*USD_TO_INR


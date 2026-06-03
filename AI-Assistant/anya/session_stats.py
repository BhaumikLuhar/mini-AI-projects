from anya.pricing import (
    calculate_cost,
    usd_to_inr
)


class SessionStats:

    def __init__(self):
        self.user_messages=0
        self.assistant_messages=0

        self.input_tokens=0
        self.output_tokens=0

        self.escalations=0


    def add_user_message(self):
        self.user_messages+=1

    def add_assistant_message(self):
        self.assistant_messages+=1

    def add_tokens(
        self,
        input_tokens,
        output_tokens
    ):
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens

    def add_escalation(self):
        self.escalations += 1

    @property
    def total_cost_usd(self):
        return calculate_cost(
            self.input_tokens,
            self.output_tokens,
            mode="production"
        )

    @property
    def total_cost_inr(self):
        return usd_to_inr(
            self.total_cost_usd
        ) 
    
    @property
    def total_messages(self):
        return (
            self.user_messages +
            self.assistant_messages
        )
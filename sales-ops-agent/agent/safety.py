MAX_ITERATIONS = 10

MAX_SESSION_COST_INR = 20.0


class SafetyManager:

    def __init__(self):

        self.iterations=0
        self.session_cost=0.0

    def check_iteration_limit(self):

        return self.iterations<MAX_ITERATIONS
    

    def increment_iteration(self):

        self.iterations+=1

    def add_cost(self,amount_inr):
        self.session_cost+=amount_inr

    def check_cost_limit(self):
        return self.session_cost<MAX_SESSION_COST_INR
    
    def get_status(self):

        return {
            "iterations":
                self.iterations,

            "cost":
                round(
                    self.session_cost,
                    2
                ),

            "iteration_limit":
                MAX_ITERATIONS,

            "cost_limit":
                MAX_SESSION_COST_INR
        }
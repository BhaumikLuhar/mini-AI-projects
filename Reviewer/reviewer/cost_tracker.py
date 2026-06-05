from dataclasses import dataclass

@dataclass
class UsageRecord:
    document_name: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost_usd: float

class CostTracker:

    def __init__(self):
        self.records=[]


    def add_record(self, record:UsageRecord):
        self.records.append(record)

    @property
    def total_input_tokens(self):
        return sum(r.input_tokens for r in self.records)

    @property
    def total_output_tokens(self):

        return sum(r.output_tokens for r in self.records)

    @property
    def total_cost_usd(self):

        return sum(r.estimated_cost_usd for r in self.records)
    

    def print_summary(self):

        print("\n")

        print("=" * 60)
        print("USAGE SUMMARY")
        print("=" * 60)

        print(
            f"Documents: "
            f"{len(self.records)}"
        )

        print(
            f"Input Tokens: "
            f"{self.total_input_tokens:,}"
        )

        print(
            f"Output Tokens: "
            f"{self.total_output_tokens:,}"
        )

        print(
            f"Estimated Cost: "
            f"${self.total_cost_usd:.4f}"
        )

        print("=" * 60)
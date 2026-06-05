from dataclasses import dataclass


@dataclass
class DocumentMetrics:
    document_name: str

    input_tokens: int = 0

    output_tokens: int = 0

    cost_usd: float = 0.0

    @property
    def total_tokens(self):

        return (
            self.input_tokens
            + self.output_tokens
        )
    
    
class MetricsCollector:

    def __init__(self):

        self.documents = {}

    def record(
        self,
        document_name,
        input_tokens,
        output_tokens,
        cost_usd,
    ):

        if document_name not in self.documents:

            self.documents[
                document_name
            ] = DocumentMetrics(
                document_name
            )

        doc = self.documents[
            document_name
        ]

        doc.input_tokens += input_tokens

        doc.output_tokens += output_tokens

        doc.cost_usd += cost_usd

    def print_summary(self):

        print()
        print("=" * 60)
        print("DOCUMENT SUMMARY")
        print("=" * 60)

        total_input = 0
        total_output = 0
        total_cost = 0

        for doc in self.documents.values():

            print(
                f"\n{doc.document_name}"
            )

            print(
                f"Input Tokens: "
                f"{doc.input_tokens:,}"
            )

            print(
                f"Output Tokens: "
                f"{doc.output_tokens:,}"
            )

            print(
                f"Cost: "
                f"${doc.cost_usd:.4f}"
            )

            total_input += (
                doc.input_tokens
            )

            total_output += (
                doc.output_tokens
            )

            total_cost += (
                doc.cost_usd
            )

        print("\n" + "=" * 60)

        print(
            f"Documents: "
            f"{len(self.documents)}"
        )

        print(
            f"Input Tokens: "
            f"{total_input:,}"
        )

        print(
            f"Output Tokens: "
            f"{total_output:,}"
        )

        print(
            f"Cost: "
            f"${total_cost:.4f}"
        )
import json
from pathlib import Path

def write_json_report(report, output_path):

    Path(output_path).write_text(
        report.model_dump_json(indent=2),
        encoding="utf-8"
    )


def render_markdown(report)->str:
    lines=[]

    lines.append(
        "# Document Review\n"
    )

    lines.append(
        "## Summary\n"
    )

    lines.append(
        report.summary + "\n"
    )

    for item in report.tldr:
        lines.append(
            f"- {item}"
        )

    lines.append("\n")

    lines.append(
        "## Document Type\n"
    )

    lines.append(
        f"{report.document_type}\n"
    )

    lines.append(
        "## Parties\n"
    )

    if report.parties:
        for party in report.parties:
            lines.append(
                f"- {party.name} ({party.role})"
            )

    else:
        lines.append(
            "- None identified"
        )

    lines.append("\n")

    lines.append(
        "## Key Dates\n"
    )

    if report.key_dates:

        for item in report.key_dates:

            lines.append(
                f"- {item.label}: {item.date}"
            )

    else:

        lines.append(
            "- None identified"
        )

    lines.append("\n")

    lines.append(
        "## Value\n"
    )

    lines.append(
        f"{report.value_inr}"
    )

    lines.append("\n")

    lines.append(
        "## Flagged Clauses\n"
    )

    if report.flagged_clauses:
        for clause in report.flagged_clauses:
            lines.append(
                f"### {clause.clause_type}"
            )

            lines.append(
                f"- Severity: {clause.severity}"
            )

            lines.append(
                f"- Concern: {clause.concern}"
            )

            lines.append(
                f"- Excerpt: {clause.excerpt}"
            )

            lines.append("")
    else:

        lines.append(
            "No flagged clauses."
        )

    lines.append("\n")

    lines.append(
        "## Confidence\n"
    )

    lines.append(
        f"{report.confidence}%"
    )

    return "\n".join(lines)



def write_markdown_report(
    report,
    output_path
):

    markdown = render_markdown(
        report
    )

    Path(
        output_path
    ).write_text(
        markdown,
        encoding="utf-8"
    )



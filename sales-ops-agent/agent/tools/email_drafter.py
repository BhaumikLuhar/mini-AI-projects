from datetime import date


def draft_email(
    recipient_name,
    recipient_email,
    company,
    context
):

    subject = (
        "Follow-up Regarding Your Inquiry"
    )

    body = f"""
Hello {recipient_name},

Thank you for your interest in our products.

{context}

Please let us know if you would like
a detailed quote or product demo.

Best regards,
Sales Team

Date: {date.today()}
"""

    return {
        "status": "approval_required",

        "approved": False,

        "recipient":
            recipient_email,

        "subject":
            subject,

        "body":
            body.strip()
    }
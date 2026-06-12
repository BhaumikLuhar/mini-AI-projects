def send_email(
    recipient: str,
    subject: str,
    body: str
):

    print(
        f"""
======== EMAIL SENT ========

TO:
{recipient}

SUBJECT:
{subject}

BODY:
{body}

============================
"""
    )

    return {
        "success": True,
        "message":
            f"Email sent to {recipient}"
    }
from anya.persona import (PersonaManager)
from anya.chat import (ChatSession)
from anya.client import (LLMClient, estimate_tokens)
from anya.commands import (handle_command)
from anya.logging_utils import (ConversationLogger)
from anya.escalation import EscalationManager
from anya.session_stats import SessionStats


def print_session_summary(
    stats
):

    print(
        "\n=== Session Summary ==="
    )

    print(
        f"Messages: "
        f"{stats.total_messages}"
    )

    print(
        f"Input Tokens: "
        f"{stats.input_tokens}"
    )

    print(
        f"Output Tokens: "
        f"{stats.output_tokens}"
    )

    print(
        f"Escalations: "
        f"{stats.escalations}"
    )

    print(
        f"Estimated Cost (USD): "
        f"${stats.total_cost_usd:.6f}"
    )

    print(
        f"Estimated Cost (INR): "
        f"₹{stats.total_cost_inr:.4f}"
    )


def main():

    manager = PersonaManager()
    logger = ConversationLogger()
    escalation_manager=EscalationManager()
    stats=SessionStats()

    persona_name = "anya"

    system_prompt = (manager.load_persona(persona_name))

    session = ChatSession(
        system_prompt
    )

    client = LLMClient()

    print(
        "\n=== Anya for AcmeCo ==="
    )

    print(
        f"Persona: {persona_name}"
    )

    print(
        "Type 'exit' to quit.\n"
    )

    while True:

        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        result = handle_command(
            user_input,
            session,
            manager
        )

        if result.should_exit:
            print_session_summary(
                stats
            )
            break

        if result.handled:
            continue

        session.add_user(
            user_input
        )
        logger.log_user(
            user_input
        )
        escalate, reason = (
            escalation_manager
            .should_escalate(
                user_input
            )
        )
        stats.add_user_message()
        user_tokens = (
            estimate_tokens(
                user_input
            )
        )

        if escalate and reason != None:

            stats.add_escalation()

            logger.log_escalation(
            reason,
            user_input
        )
            print(
            "\nAnya: "
            "Your request has been "
            "escalated to a human "
            "support representative."
        )
            
        if (escalation_manager.stop_conversation):
            break

        print("\nAnya: ",end="")

        reply = (
            client.stream_reply(
                session.get_messages()
            )
        )

        confidence = (
            client.assess_confidence(
                user_input,
                reply
            )
        )

        if escalation_manager.low_confidence(confidence):

            stats.add_escalation()

            logger.log_escalation(
                f"low-confidence:{confidence}",
                user_input
            )

            print(
                "\n[Escalation]"
                " This answer has been "
                "flagged for human review."
            )
      

        session.add_assistant(
            reply
        )
        logger.log_assistant(
            reply
        )
        stats.add_assistant_message()
        assistant_tokens = (
            estimate_tokens(
                reply
            )
        )

        stats.add_tokens(user_tokens,assistant_tokens)

        print(
            f"\n[Messages: "
            f"{stats.total_messages}"
            f" | Tokens: "
            f"{stats.input_tokens + stats.output_tokens}"
            f" | Cost: ₹"
            f"{stats.total_cost_inr:.4f}]"
        )

    print(
        "\nGoodbye."
    )


if __name__ == "__main__":
    main()
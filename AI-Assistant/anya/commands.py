from dataclasses import dataclass


@dataclass
class CommandResult:
    handled: bool = False
    should_exit: bool = False

    
def handle_command(user_input, session, persona_manager):

    if not user_input.startswith("/"):
        return CommandResult(
            handled=False
        )
    
    if user_input == "/reset":

        session.reset()

        print(
            "\nConversation reset."
        )

        return CommandResult(
            handled=True
        )
    
    if user_input == "/save":

        filename = session.save()

        print(
            f"\nSaved: {filename}"
        )

        return CommandResult(
            handled=True
        )
    
    if user_input.startswith("/load "):
        parts = user_input.split(maxsplit=1)

        if len(parts!=2):
            print("Usage: /load <file>")

            return CommandResult(
                handled=True
            )
        
        filename=parts[1]

        try:

            session.load(
                filename
            )

            print(
                "\nConversation loaded."
            )

        except FileNotFoundError:

            print(
                "\nFile not found."
            )

        return CommandResult(
            handled=True
        )
    

    if user_input.startswith("/persona"):
        parts=user_input.split(maxsplit=1)

        if(len(parts)!=2):
            print("Usage: /persona <name>")

            return CommandResult(
                handled=True
            )
        
        persona_name=parts[1]

        if not persona_manager.persona_exists(persona_name):
            print("Persona not found.")

        prompt = (persona_manager.load_persona(persona_name))

        session.system_prompt = prompt
        session.reset()
        print(f"Switched to: {persona_name}")

        return CommandResult(
                handled=True
            )
    

    if user_input == "/agent":

        prompt = (
            persona_manager
            .load_persona("agent")
        )

        session.system_prompt = prompt
        session.persona_name="agent"
        session.reset()

        print(
            "\nSwitched to "
            "Agent Mode."
        )

        return CommandResult(
            handled=True
        )
    

    if user_input == "/quit":

        return CommandResult(
            handled=True,
            should_exit=True
        )
    
    print("\nUnknown command.")

    return CommandResult(
        handled=True
    )
    
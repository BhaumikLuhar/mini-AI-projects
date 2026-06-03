# anya/persona.py

from pathlib import Path

PERSONA_DIR = Path("personas")


class PersonaManager:
    """
    Handles persona discovery and loading.
    """

    def __init__(self):
        self.persona_dir = PERSONA_DIR

    def list_personas(self) -> list[str]:
        """
        Return all available persona names.
        """

        return sorted(
            file.stem
            for file in self.persona_dir.glob("*.txt")
        )

    def persona_exists(self, name: str) -> bool:
        """
        Check whether a persona exists.
        """

        return (
            self.persona_dir / f"{name}.txt"
        ).exists()

    def load_persona(self, name: str) -> str:
        """
        Load persona content.
        """

        persona_file = (
            self.persona_dir / f"{name}.txt"
        )

        if not persona_file.exists():
            raise FileNotFoundError(
                f"Persona '{name}' not found."
            )

        return persona_file.read_text(
            encoding="utf-8"
        )
from pydantic import ValidationError

from agent.schemas import (
    CRMLookupInput,
    InventoryInput,
    SearchInput,
    QuoteInput,
    EmailDraftInput,
    ListInventoryInput,
    FindProductInput
)

SCHEMA_MAP = {

    "crm_lookup":
        CRMLookupInput,

    "check_inventory":
        InventoryInput,

    "web_search":
        SearchInput,

    "calculate_quote":
        QuoteInput,

    "draft_email":
        EmailDraftInput,

    "list_inventory":
        ListInventoryInput,

    "find_product":
        FindProductInput
}


def validate_tool_input(tool_name:str, tool_input:dict):
    try:
        schema=SCHEMA_MAP.get(tool_name)

        if not schema:
            return {
                "valid": False,
                "error":
                    f"Unknown tool: {tool_name}"
            }

        validated=schema.model_validate(tool_input)

        return {
            "valid":True,
            "data": validated.model_dump()
        }
    
    except ValidationError as e:
        return {
            "valid":False,
            "error":e.errors()
        }
from .crm import crm_lookup
from .inventory import check_inventory
from .pricing import calculate_quote
from .email_drafter import draft_email
from .search import web_search
from .catalog import list_inventory
from .find_product import find_product
from .send_email import send_email

TOOL_FUNCTIONS = {
    "crm_lookup": crm_lookup,

    "check_inventory": check_inventory,

    "calculate_quote": calculate_quote,

    "draft_email": draft_email,

    "web_search": web_search,

    "list_inventory": list_inventory,

    "find_product": find_product,

    "send_email": send_email
}
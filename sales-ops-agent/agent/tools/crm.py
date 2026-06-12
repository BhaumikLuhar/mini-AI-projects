import json
from pathlib import Path

data_path=(Path(__file__).parent.parent.parent / "data" / "leads.json")


def crm_lookup(email:str):

    with open(data_path,"r",encoding="utf-8")as f:
        leads=json.load(f)

    for lead in leads:

        if lead["email"].lower()==email.lower():
            return {
                "found": True,
                "lead": lead
            }
        
    return {
        "found":False,
        "message": (f"No lead found for {email}")
    }
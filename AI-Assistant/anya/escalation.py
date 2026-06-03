import json
from pathlib import Path

class EscalationManager:

    def __init__(self,config_file="escalation_rules.json"):
        with open(config_file,"r",encoding="utf-8")as f:
            self.rules=json.load(f)

        self.keywords=self.rules["keywords"]

        self.abusive_words=self.rules["abusive_words"]

        self.stop_conversation=self.rules["stop_conversation"]

        self.confidence_threshold=self.rules["confidence_threshold"]


    def check_keyword(self,message:str):
        text=message.lower()

        for word in self.keywords:
            if word.lower() in text:
                return (True, f"keyword: {word}")

        return False,None


    def check_abuse(self,message:str):
        text=message.lower()

        for word in self.abusive_words:
            if word.lower() in text:
                return (True, f"abuse: {word}")

        return False,None
    

    def should_escalate(self,message:str):

        escalate, reason=self.check_keyword(message)

        if escalate:
            return True, reason
        
        escalate, reason=self.check_abuse(message)

        if escalate:
            return True, reason
        
        return False, None
            

    def low_confidence(self,score):
        return (
            score
            <= self.confidence_threshold
        )
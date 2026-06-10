import json

from datetime import datetime

from chatdocs.constants import (
    DEFAULT_INDEX_STATE
)

class StateManager:

    def __init__(self, state_file=DEFAULT_INDEX_STATE):
        self.state_file=state_file

    
    def load(self):

        if not self.state_file.exists():
            return {}

        with open(self.state_file,"r",encoding="utf-8")as f:
            return json.load(f)

    
    def save(self, state):
        with open(self.state_file,"w",encoding="utf-8")as f:
            json.dump(state,f,indent=2)


    def update_file(self,source_name,file_hash):
        state=self.load()
        
        state[source_name]={
            "hash":file_hash,
            "indexed_at":datetime.utcnow().isoformat()
        }

        self.save(state)


    def remove_file(self,source_name):
        state=self.load()

        if source_name in state:
            del state[source_name]

        self.save(state)


    def get_hash(self, source_name):
        state=self.load()

        record=state.get(source_name)

        if not record:
            return None
        
        return record["hash"]


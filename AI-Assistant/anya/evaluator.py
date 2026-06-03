import json
from pathlib import Path

class Evaluator:

    def __init__(self,dataset_path):
        with open(dataset_path,"r",encoding="utf-8")as f:
            self.tests=json.load(f)


    def check_expected_phrases(self,response,expected_phrases):
        response=response.lower()
        matches=0

        for phrase in expected_phrases:
            if phrase.lower() in response:
                matches+=1

        return matches==len(expected_phrases)
    

    def run_test(self, client, system_prompt, test_case):

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content":
                test_case["question"]
            }
        ]

        response = (client.get_reply(messages))

        passed = (
            self.check_expected_phrases(
                response,
                test_case[
                    "expected_phrases"
                ]
            )
        )

        return {
            "question":
                test_case["question"],
            "passed":
                passed,
            "response":
                response
        }
    

    def run_all(self, client, system_prompt):

        results=[]

        for test in self.tests:
            result=self.run_test(client, system_prompt, test)
            results.append(result)

        return results
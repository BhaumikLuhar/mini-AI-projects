import os

import requests

old_request = requests.Session.request

def new_request(self, *args, **kwargs):
    kwargs["verify"] = False
    return old_request(self, *args, **kwargs)

requests.Session.request = new_request
from agent.config import get_tavily_key
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client=TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def web_search(query:str):

    try:
        response=client.search(
            query=query,
            search_depth="basic",
            max_results=5,
            verify=False
        )

        results=[]

        for item in response.get("results",[]):
            results.append(
                {
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "content": item.get("content")
                }
            )

        return {
            "success": True,
            "query": query,
            "results": results
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
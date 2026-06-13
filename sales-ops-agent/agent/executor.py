from agent.validation import validate_tool_input
from agent.tools.init import TOOL_FUNCTIONS
from agent.logging_utils import log_tool_call
import time

def execute_tool(tool_name:str,tool_input:dict):

    validation=validate_tool_input(tool_name,tool_input)

    if not validation["valid"]:

        return {
            "success": False,
            "error":
                "Validation Failed",
            "details":
                validation["error"]
        }
    
    tool_function=TOOL_FUNCTIONS.get(tool_name)

    if not tool_function:

        return {
            "success": False,
            "error":
                f"Tool not found: {tool_name}"
        }
    
    start_time=time.time()

    try:
        result=tool_function(**validation["data"])

        latency=round((time.time()-start_time)*1000,2)
        try:
            log_tool_call(tool_name,tool_input,result,latency)
        except Exception:
            pass

        print(
            f"\n[TOOL CALL]"
            f"\nTool: {tool_name}"
            f"\nInput: {tool_input}\n"
        )

        return {
            "success": True,
            "tool_name": tool_name,
            "input": tool_input,
            "result": result
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
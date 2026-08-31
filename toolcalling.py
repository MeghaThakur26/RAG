from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage

from rich import print

# 1. Creating a tool --  getting the length 
@tool
def get_text_length(text: str) -> int:
    """ return the number of character in a given text """
    return len(text)

tools = {
    "get_text_length": get_text_length     #tool calling - give all the tools you have
}
#2.  LLM
llm = ChatMistralAI(model = "mistral-small-2603")

#3.  TOOL BINDING -- LLM with tools
llm_tools = llm.bind_tools([get_text_length]) #pass all the tools you have created in a list

message = []

prompt = input(" You:")  # user input
query = HumanMessage(prompt)
message.append(query)

result = llm_tools.invoke(message)  # this gives AI MESSAGE
message.append(result)


# check if we have any tool call if yes then we will extract the tool name -- we dont know which tool to use so we will extract the tool name.
if result.tool_calls:
    tool_name = result.tool_calls[0]["name"]
    tool_meesage = tools[tool_name].invoke(result.tool_calls[0])   # we are calling the tools which have all the tools in it with the toolname we will use
    message.append(tool_meesage)
    print(message)

result = llm_tools.invoke(message)
print(result.content)
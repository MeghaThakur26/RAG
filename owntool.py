from langchain.tools import tool 

@tool                                     # decorator its like a wrapper that wrapped the tool inside it
def get_greeting(name: str) -> str:        #type hints
    """ Generate a greeting message for a user """          #tells what this function do to llm - docstring
    return f"Hello {name},Welcome to the AI world"


result =get_greeting.invoke({"name":"megha"})
print(result)
print(get_greeting.name)
print(get_greeting.description)
print(get_greeting.args)
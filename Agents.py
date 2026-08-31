# First step - loading all the libraries

from dotenv import load_dotenv
load_dotenv()
import os
import requests  #used to make HTTP requests to websites and APIs.

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient
from rich import print

#Now lets create some tools 

#Weather tool

@tool
def get_weather(city: str) ->str:
    """ Get current weather of a city """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    print("DEBUG:",data)
    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Could not fetch weather')}"
    
    temp = data["main"]["temp"] #disctionary
    desc = data["weather"][0]["description"] # its a list so indexing is needed
    
    return f"Weather in {city}: {desc}, {temp}°C"

# Tavily news tool

tavily_client =  TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def get_news(city : str) -> str:
    """ Get the latest news about the city """

    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )
    
    results = response.get("results", [])
    print(results)
    if not results:
        return f"No news found for {city}"
    
    news_list = []
    
    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")
        
        news_list.append(
            f"- {title}\n  🔗 {url}\n  📝 {snippet[:100]}..."
        )
    
    return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)

print(get_news.invoke("dehli"))

# Create llm and bind

llm = ChatMistralAI(model="mistral-small-2603")

tools = {"get_weather": get_weather,
         "get_news" : get_news}

llm_tools = llm.bind_tools([get_weather,get_news])

# AGENT LOOP 
messages = []
print("City intelligence system")
print("type Exit to quit")

while True:
    user_input = input("You: ")
    if user_input.lower()== "exit":
        break
    messages.append(HumanMessage(user_input))

    while True:
        result = llm_tools.invoke(messages)
        messages.append(result)        # this give AI message

        #check if tool is required or not.
        if result.tool_calls:
            for tool_call in result.tool_calls:   # now we have two tools and if user gives a query that uses both the tools.
                tool_name = tool_call['name']

                #Human in the loop
                confirm = input(f"Agent want to call {tool_name} Approve(y/n)")
                if confirm.lower()== "n":
                    print("Tool call denied, I cannot get the latest information ")
                    break

                #execute the tool
                tool_result = tools[tool_name].invoke(tool_call)

                messages.append(ToolMessage(content = tool_result, tool_call_id = tool_call["id"]))

            continue
        else:
            print("/n" "Final Answer:" "/n")
            print(result.content)
            print("/n" + "="*50 + "/n")
            break
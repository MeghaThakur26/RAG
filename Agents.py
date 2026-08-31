
# ============================================================
# AGENTS.PY
# ============================================================

# First step - loading all libraries

from dotenv import load_dotenv
load_dotenv()

import os
import requests

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient
from rich import print


# ============================================================
# WEATHER TOOL
# ============================================================

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city."""

    api_key = os.getenv("OPENWEATHER_API_KEY")

    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city},IN&appid={api_key}&units=metric"
    )

    response = requests.get(url)

    data = response.json()

    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Could not fetch weather')}"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"Weather in {city}: {desc}, {temp}°C"


# ============================================================
# TAVILY CLIENT
# ============================================================

tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


# ============================================================
# NEWS TOOL
# ============================================================

@tool
def get_news(city: str) -> str:
    """Get the latest news about the city."""

    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )

    results = response.get("results", [])

    if not results:
        return f"No news found for {city}"

    news_list = []

    for r in results:

        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")

        news_list.append(
            f"- {title}\n"
            f"  🔗 {url}\n"
            f"  📝 {snippet[:100]}..."
        )

    return (
        f"Latest news in {city}:\n\n"
        + "\n\n".join(news_list)
    )


# ============================================================
# LLM
# ============================================================

mistral_key = os.getenv("MISTRAL_API_KEY")

if not mistral_key:
    raise ValueError(
        "MISTRAL_API_KEY is not configured."
    )

print("MISTRAL_API_KEY found")

llm = ChatMistralAI(
    model="mistral-small-2603"
)


# ============================================================
# TOOLS
# ============================================================

tools = {
    "get_weather": get_weather,
    "get_news": get_news
}


# ============================================================
# LLM + TOOLS
# ============================================================

llm_tools = llm.bind_tools(
    [
        get_weather,
        get_news
    ]
)


# ============================================================
# TERMINAL AGENT
# ============================================================

def run_terminal_agent():

    messages = []

    print("City intelligence system")
    print("Type Exit to quit")

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        messages.append(
            HumanMessage(content=user_input)
        )

        while True:

            result = llm_tools.invoke(messages)

            messages.append(result)

            # ------------------------------------------------
            # TOOL CALL
            # ------------------------------------------------

            if result.tool_calls:

                for tool_call in result.tool_calls:

                    tool_name = tool_call["name"]

                    # ----------------------------------------
                    # HUMAN IN THE LOOP
                    # ----------------------------------------

                    confirm = input(
                        f"Agent wants to call "
                        f"{tool_name}. Approve (y/n): "
                    )

                    if confirm.lower() == "n":

                        print(
                            "Tool call denied. "
                            "I cannot get the latest information."
                        )

                        break

                    # ----------------------------------------
                    # EXECUTE TOOL
                    # ----------------------------------------

                    tool_result = tools[
                        tool_name
                    ].invoke(tool_call)

                    messages.append(
                        ToolMessage(
                            content=str(tool_result),
                            tool_call_id=tool_call["id"]
                        )
                    )

                continue

            # ------------------------------------------------
            # FINAL ANSWER
            # ------------------------------------------------

            else:

                print("\nFinal Answer:\n")

                print(result.content)

                print("\n" + "=" * 50 + "\n")

                break


# ============================================================
# ONLY RUN TERMINAL AGENT WHEN THIS FILE IS EXECUTED DIRECTLY
# ============================================================

if __name__ == "__main__":

    run_terminal_agent()

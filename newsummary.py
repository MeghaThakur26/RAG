from dotenv import load_dotenv
#from langchain_community.tools.tavily_search import TavilySearchResult
from langchain_tavily import TavilySearch
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

tool = TavilySearch(
    max_results=5,
    topic="general",
)

llm = ChatMistralAI(model = "mistral-small-2603")

prompt = ChatPromptTemplate.from_template(
    """ You are a helpfull assitant
    summarize the fooloeing new into clear bullet points
    {news}
"""
)
chain = prompt | llm | StrOutputParser()


result = tool.run("Latest AI news of 2026")
response = chain.invoke({"news": result})

print(response)
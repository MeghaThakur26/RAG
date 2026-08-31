from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnableLambda

# Components
model = ChatMistralAI(model="mistral-small-2506")
parser = StrOutputParser()

# Two different prompts
short_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in 1-2 lines"
)

detailed_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in detail"
)

# Input
topic = "Machine Learning"

chain = RunnableParallel({          
    "short": RunnableLambda(lambda x : x['short']) |short_prompt | model | parser ,           # Runnable lambda - now our runnable is confused as it is getting dictinary as inout instead of topic
    "detailed" : RunnableLambda(lambda x : x['detailed']) |detailed_prompt |model |parser    # we extracting the short/detailed from the dictionary chain.invoke
})

result = chain.invoke({ "short":{"topic":"Machine Learning"}, #giving the input in dictionary as we can have multiple inputs in short and detail
                         "detailed":{"topic": "Deep learning"}
                       })
                       

print(result["short"])
print(result["detailed"])
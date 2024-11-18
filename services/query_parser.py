from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openApiKey = os.getenv("OPENAPI_KEY")

# Initialize LangChain components
prompt_template = """
You are a helpful assistant for room availability queries. 
A user might ask about rooms in various locations and dates.
Extract the date and location from the following query: "{query}"
"""

prompt = PromptTemplate(input_variables=["query"], template=prompt_template)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, openai_api_key="openApiKey")
llm_chain = LLMChain(prompt=prompt, llm=llm)

def parse_query(query: str):
    """
    Use LangChain to parse a natural language query and extract location and date.
    """
    response = llm_chain.run(query)
    try:
        location, date = response.split(",")
        location = location.split(":")[1].strip()
        date = date.split(":")[1].strip()
        return location, date
    except Exception as e:
        raise ValueError("Could not extract location or date.")

import os
from langchain_openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
API_SECRET_KEY = "sk-f29A4tQuVfHMbdcgqHrNIF3QRVJmbpnrqucE7V7062r4fz8L"
BASE_URL = "https://api.f2gpt.com/v1" 
os.environ["OPENAI_API_KEY"] = API_SECRET_KEY
os.environ["OPENAI_API_BASE"] = BASE_URL
# llm = OpenAI(temperature=0.9)

prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")
model = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.9)
output_parser = StrOutputParser()

chain = prompt | model | output_parser

response= chain.invoke({"topic": "ice cream"})

print(response)
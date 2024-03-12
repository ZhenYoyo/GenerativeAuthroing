import os
from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

API_SECRET_KEY = "sk-f29A4tQuVfHMbdcgqHrNIF3QRVJmbpnrqucE7V7062r4fz8L"
BASE_URL = "https://api.f2gpt.com/v1" 
os.environ["OPENAI_API_KEY"] = API_SECRET_KEY
os.environ["OPENAI_API_BASE"] = BASE_URL
llm = OpenAI(temperature=0.9)


loader = WebBaseLoader("https://paperarchipelago.wordpress.com/technical-log/")
docs = loader.load()
embeddings = OpenAIEmbeddings()


text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)

prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
])


retriever = vector.as_retriever()
retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

chat_history = [
    HumanMessage(content="love you"),
    AIMessage(content="love you too")
]

retriever_chain.invoke({
    "chat_history": chat_history,
    "input": "I love you"
})

prompt1 = ChatPromptTemplate.from_messages([
    ("system", "Answer the following question based only on the provided context:\n\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
])
document_chain = create_stuff_documents_chain(llm, prompt1)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)
# document_chain = create_stuff_documents_chain(llm, prompt)

chat_history = [HumanMessage(content="So what is the island"), AIMessage(content="A beautiful place maybe")]
response = retrieval_chain.invoke({
    "chat_history": chat_history,
    "input": "Tell me how"
})


print(response["answer"])
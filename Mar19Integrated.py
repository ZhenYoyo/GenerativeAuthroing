import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai.embeddings import OpenAIEmbeddings

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

#------
# ---- full debug
#import langchain 
#langchain.debug = True
#-------

#-----
#defining api key
API_SECRET_KEY = "sk-f29A4tQuVfHMbdcgqHrNIF3QRVJmbpnrqucE7V7062r4fz8L"
BASE_URL = "https://api.f2gpt.com/v1" 
os.environ["OPENAI_API_KEY"] = API_SECRET_KEY
os.environ["OPENAI_API_BASE"] = BASE_URL
#-----
#defining model
model = ChatOpenAI(model="gpt-3.5-turbo", verbose=True)
#-----

#---
#defining world setting, character, narrator behavior, input variables for differenve narrative stages--page1
narrator_behavior_list = []
input_variables_list = []
input_variables_demonstration = []
narrative_retrieval_list = []

#---
# for page 2, template state machine
prompttemplate_list = []
formatted_retrieval_list = []
currentprompt = ""

#----
#this should not be changes, is for summarizing the chat history -- page3
contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""

chat_history = []

#for switching stages
stage = 0

#------



# for page-2 to 3, add new item to RunnableParallel
class RunnableParallel:
    def __init__(self, items):
        self.items = items

    def add_item(self, key, value):
        self.items[key] = value




while True:

    user_input = input("<+ ")

    if not user_input:
        continue


    #-----PAGE1
    #adding the narrative setting and character

    if user_input.startswith("world>"):
      narrative_retrieval_list.append("worldsetting:"+user_input[6:] + "\n")
      print("narrative_retrieval_list:", narrative_retrieval_list)
    if user_input.startswith("character>"):
      narrative_retrieval_list.append("character:"+ user_input[10:]+ "\n")
      print("narrative_retrieval_list:", narrative_retrieval_list)

    #adding narrator behaviors
    if user_input.startswith("narratorbehavior>"):
        narrator_behavior_list.append(user_input[17:]+ "\n")
        print("narrator_behavior_list:", narrator_behavior_list)


    #adding input variables and their functions
    if user_input.startswith("inputvariable>"):
        #input must be in the form of "{lightintensity} is changing the emotional tone of the story", {lightintensity} is the input variable
        new_input_variable = user_input[14:]
        input_variables_list.append(new_input_variable)
        description = input("defining this input:")
        input_variables_demonstration.append("{"+new_input_variable+"}"+ description)
        print("input_variables_list:", input_variables_list)
        print("input_variables_demonstration:", input_variables_demonstration)

    #-----PAGE2
    # defining the combinations for different narrative stages
    #! 这里有一个问题是现在的1, 2 是写定的, 要想怎么跟按钮联系起来, 按下按钮之后添加一个input stage/ 或者或多个input stage-- 可能是list同时多个item的问题
    if user_input.startswith("branching>"):   
        inputstage1_index = int(input("input_stage1:"))
        inputstage1 = input_variables_list[inputstage1_index] 
        inputstage1_demonstration = input_variables_demonstration[inputstage1_index]

        inputstage2_index = int(input("input_stage2:"))
        inputstage2 = input_variables_list[inputstage2_index] 
        inputstage2_demonstration = input_variables_demonstration[inputstage2_index]

        #put numer here, 0 for picking out the first item from the list
        #！这里有点问题, 理论上要支持添加多个narrative elements, 但是这里只支持每次给一个阶段的narrative添加一条
        narrative_1 = narrative_retrieval_list[int(input("narrative_1:"))]
        narrative_2 = narrative_retrieval_list[int(input("narrative_2:"))]

        prompttemplate_list.insert(0, narrator_behavior_list[0] + "This is the story context you are based from:{context} \ generate narrative based on player's input: {question}. " + inputstage1_demonstration)
        formatted_retrieval_list.insert(0, narrative_1)
        
        prompttemplate_list.insert(1, narrator_behavior_list[1] + "This is the story context you are based from:{context} \ generate narrative based on player's input: {question}. " + inputstage2_demonstration)
        formatted_retrieval_list.insert(1, narrative_2)

        print("prompttemplate_list:", prompttemplate_list)
        print("formatted_retrieval_list:", formatted_retrieval_list)
        #print("inputstage1:", inputstage1, "inputstage2:", inputstage2, "narrative_1:", narrative_1, "narrative_2:", narrative_2)

        
        
 


    #-----PAGE3
    #run the game-page3
        
    #simulating narrative stage 1
    if user_input.startswith("start>"):
    #-------
    #docs/file/retrieval -- load and embedding knowledge for world setting and character
        vectorstore = DocArrayInMemorySearch.from_texts(
        formatted_retrieval_list[stage],
        embedding=OpenAIEmbeddings(),
        )
        retriever = vectorstore.as_retriever()
    #-- ----
        while True:
            question = input("Player: ")

            #will change based on the types of input chose before
            currentinput = input_variables_list[stage]
            currentinput_value= input(currentinput+":")
            print(currentinput, currentinput_value)
            
            if question == "switchstage":
                 stage = input(int("narrative stage:"))
    
                 vectorstore = DocArrayInMemorySearch.from_texts(
                 # narrative_retrieval_list,
                 formatted_retrieval_list[stage],
                 embedding=OpenAIEmbeddings(),
                 )   
                 retriever = vectorstore.as_retriever()
            
            contextualize_q_prompt = ChatPromptTemplate.from_messages(
                [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
                ]
            )
            contextualize_q_chain = contextualize_q_prompt | model | StrOutputParser()
            #-----

            prompt = ChatPromptTemplate.from_messages(
                [
                ("system", prompttemplate_list[stage]),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
                ]
            )


            def contextualized_question(input: dict):
                if input.get("chat_history"):
                    return contextualize_q_chain
                else:
                    return input["question"]


            #!!!###   
            setup_and_retrieval = RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
            setup_and_retrieval.add_item(currentinput, RunnablePassthrough())

            rag_chain = (
                RunnablePassthrough.assign(
                context=contextualized_question | retriever 
            )
                | prompt
                | model
            )


            invoke_dict = {"question": question, "chat_history": chat_history}
            invoke_dict[currentinput] =  currentinput_value # 添加新的键值对
            
            #ai_msg = rag_chain.invoke({"question": question, "chat_history": chat_history})
            ai_msg = rag_chain.invoke(invoke_dict)
            chat_history.extend([HumanMessage(content=question), AIMessage(content=ai_msg.content)])
            print("narrative:", ai_msg.content)
            #print if check the chat history
            #print("chat history:", chat_history)
from flask import Flask, render_template, request, jsonify
import openai
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
import json

# from flask_socketio import SocketIO, emit

#currently we can apply our own key, but later need to public this to let user to put their own key
#defining api key
API_SECRET_KEY = "sk-f29A4tQuVfHMbdcgqHrNIF3QRVJmbpnrqucE7V7062r4fz8L"
BASE_URL = "https://api.f2gpt.com/v1" 
os.environ["OPENAI_API_KEY"] = API_SECRET_KEY
os.environ["OPENAI_API_BASE"] = BASE_URL
#-----
#defining model
model = ChatOpenAI(model="gpt-3.5-turbo", verbose=True)
#-----


input_variables_list = []
input_variables_demonstration = []
worldsetting_list = []
character_list = []
narrator_behavior_list = []

variable_dic = {}

#for page2 card creation
worldsetting_list_no = 0
character_list_no = 0
narrator_behavior_list_no = 0
input_variables_list_no = 0



#***for defining the dictionary output, what we will use in the real narrative-- page2
narrating_dic = {}

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


#oringinal
player_input = ""
external_input = ""



class RunnableParallel:
    def __init__(self, items):
        self.items = items

    def add_item(self, key, value):
        self.items[key] = value


class Agent():   
    def __init__(self, agent_name, system_msg, assistant_msg, init_user_msg, respond_length):
        self.agent_name = agent_name
        self.system_msg = system_msg
        self.assistant_msg = assistant_msg
        self.init_user_msg = init_user_msg
        self.respond_length = respond_length
        self.messages = [{"role": "assistant", "content": assistant_msg},
                         {"role": "user", "content": init_user_msg}]
        self.debug_mode = False 

    def get_completion(self, model="gpt-3.5-turbo", temperature=0.8):
        #global total_tokens
        messages = self.messages
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        self.messages.append({"role": "assistant", "content": response.choices[0].message["content"]})
        self.total_tokens = response.usage["total_tokens"]
        #print("Total tokens:", total_tokens)

        if self.debug_mode:
            #return response
            return messages
        else:
            return response.choices[0].message["content"]
narrator = Agent("narrator", 
                      '',
                      "Hi, I'm the narrator.", 
                      '', 
                      "30")


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

#---for page1
@app.route('/world', methods=['POST', 'GET'])
def system():
    global worldsetting_list
    global character_list
    global input_variables_list 
    global input_variables_demonstration
    global variable_dic

    global narrator_behavior_list
    global newkey

    input_data = request.json
    if input_data['id'] == 1:
        worldsetting_list.append(input_data['text'])
        print(worldsetting_list)  # Printing the result on the server console
        
    elif input_data['id'] == 2:
        character_list.append(input_data['text'])
        print(character_list)  

    elif input_data['id'] == 5:
        narrator_behavior_list.append(input_data['text'])
        print(narrator_behavior_list)  
    

    #create a dictionary to store the variable and description
    elif input_data['id'] == 3:
       #modified
       input_variables_list.append(input_data['text'])
       print(input_variables_list )  
       newkey= input_data['text']

    elif input_data['id'] == 4:
       input_variables_demonstration.append(input_data['text'])
       print(input_variables_demonstration)  
       newkeyvalue= input_data['text']

       variable_dic[newkey] = newkeyvalue
       print(variable_dic)  # Printing the result on the server console
    
    # Printing the result on the server console
    # Process the input data and generate output
    # Send the result to the client-side JavaScript as a JSON response
    return jsonify({'output': ''})


@app.route('/removeworld', methods=['POST'])
def removesystem():
    global worldsetting_list
    global character_list
    global input_variables_list 
    global input_variables_demonstration
    global variable_dic
    global narrator_behavior_list

    data = request.json
    # if data['id'] == 1:
    #     worldsetting_list.remove(data['value'])
    #     print(worldsetting_list)  # Printing the result on the server console

    if data['id'] == 1:
     if data['value'] in worldsetting_list:
        worldsetting_list.remove(data['value'])
        print(worldsetting_list)
     else:
        print(f"{data['value']} no existi")
        
    elif data['id'] == 2:
        character_list.remove(data['value'])
        print(character_list)  # Printing the result on the server console

    elif data['id'] == 5:
        narrator_behavior_list.remove(data['value'])
        print(narrator_behavior_list)  


    elif data['id'] == 3:
        del variable_dic[data['value']]
        print(variable_dic) # Printing the result on the server console
        
    # Send the result to the client-side JavaScript as a JSON response
    return jsonify({'output': ''})


@app.route('/worldcard')
def get_data1():
    global worldsetting_list
    global worldsetting_list_no
    worldsetting_list_no = len(worldsetting_list)
    #print("wordcardno", worldsetting_list_no)
    data = {'value': worldsetting_list_no, 'worldlist': worldsetting_list}
    return jsonify(data)


@app.route('/charactercard')
def get_data2():
    global character_list
    global character_list_no
    character_list_no = len(character_list)
    #print("charactercardno", character_list_no)
    data = {'value': character_list_no, 'characterlist': character_list}
    return jsonify(data)


@app.route('/narratorcard')
def get_data3():
    global narrator_behavior_list
    global narrator_behavior_list_no
    narrator_behavior_list_no = len(narrator_behavior_list)
    #print("narratorno", narrator_behavior_list_no)
    data = {'value': narrator_behavior_list_no, 'narratorlist': narrator_behavior_list}
    return jsonify(data)

@app.route('/inputcard')
def get_data4():
    global variable_dic
    global input_variables_list_no
    global input_variables_demonstration
    input_variables_list_no = len(variable_dic)
    #print("inputno", input_variables_list_no)
    data = {'value': input_variables_list_no, 'inputlist': input_variables_demonstration}
    return jsonify(data)



#---for page2

@app.route('/branching', methods=['POST', 'GET'])
# TO DO @Warren: This route should be used to update the narrating_dic dictionary
#here is for building a dictionary to store the systemprompt and the retrievel list
# @app.route('/branching', methods=['POST', 'GET'])
#global narrating_dic
#narrating_dic["initial narrative stage"]={"systemprompt": narrator_behavior_list[0] + input_variables_list[0]+input_variables_demonstration[0], "retrieval": worldsetting_list[0]+character_list[0]}
#key是根据html里接受的string来设置的, SYSTEMPROMPT是当前输入的behavior和inputvariable的拼贴, RETRIEVAL是当前输入的worldsetting和character的拼贴



# Ideally, the outcome of this route is updating narrating_dic = {}



#---for page3

# @app.route('/process')
@app.route('/process', methods=['POST'])
def process():
     
     global narrating_dic 
     global player_input
     global external_input
     global start

     input_data = request.json

     if input_data['id'] == 1:
        player_input = input_data['text']
        print("playerinput", player_input)  # Printing the result on the server console
        start = ""
        
     elif input_data['id'] == 2:
        external_input = input_data['text']
        print("externalinput", external_input)  # Printing the result on the server console
        start = ""
     elif input_data['id'] == 5:
        start = input_data['text']
        print("start", start)  # Printing the result on the server console

     else:
        start = ""

    #  print(player_input)

     return jsonify({'output': ''})


    #  prompt_must_have = "This is the story context you are based from:{context} \ generate narrative based on player's input: {question}. " 
     # for demo, the real one will be updated in real time

     # need to solve how to automatically add "{}" for input variable

    #  narrating_dic = {"initial narrative stage": {"systemprompt": prompt_must_have + narrator_behavior_list[0] + "{"+input_variables_list[0]+"}"+input_variables_demonstration[0], 
    #                                        "retrieval": worldsetting_list[0]+character_list[0]},

    #                    "second narrative stage": {"systemprompt": prompt_must_have + narrator_behavior_list[1] + "{"+ input_variables_list[1]+"}"+input_variables_demonstration[1],
    #                                        "retrieval": worldsetting_list[1]+character_list[1]},

    #                    "third narrative stage": {"systemprompt": prompt_must_have + narrator_behavior_list[2] + "{"+ input_variables_list[2]+ "}"+input_variables_demonstration[2],
    #                                        "retrieval": worldsetting_list[2]+character_list[2]}
    #                  }
    


#      setting1= "Enchanted Forest: A mystical forest shrouded in enchantment, with towering ancient trees, sparkling streams, and glowing flora. Sunlight filters through the dense canopy, casting ethereal hues across the landscape. Magical creatures roam freely, and whispers of forgotten spells fill the air."
#      setting2= "A bustling metropolis of gleaming skyscrapers, advanced technology, and neon lights. Flying cars zip through the skies, holographic advertisements dance on every corner, and automated drones navigate the cityscape. The atmosphere hums with energy and innovation."
#      setting3= "Decaying ruins of a long-lost civilization, nestled deep within an overgrown jungle. Crumbling stone structures, intricate carvings, and moss-covered artifacts tell tales of a forgotten era. The air is heavy with mystery and echoes of the past."
#      behavior1= "Descriptive: The narrator provides vivid descriptions of the surroundings, characters, and events, painting a detailed picture for the audience. They engage the audience's senses by describing sights, sounds, smells, and textures."
#      behavior2= "Engaging: The narrator uses a dynamic and expressive tone, capturing the audience's attention and creating a sense of excitement. They employ rhetorical questions, exclamations, and varying pacing to keep the audience engaged and interested."
#      behavior3= "Reflective: The narrator offers introspective and contemplative insights, delving into the characters' thoughts and emotions. They provide commentary on the themes and deeper meanings of the story, encouraging the audience to reflect on the narrative's messages."

#      narrating_dic = {"initial narrative stage": {"systemprompt": behavior1, 
#                                            "retrieval": setting1},

#                        "second narrative stage": {"systemprompt": behavior2,
#                                            "retrieval": setting2},

#                        "third narrative stage": {"systemprompt": behavior3
# ,
#                                            "retrieval": setting3}
#                     }
     

     
# #start
#      if start == "generate":   
#         vectorstore = DocArrayInMemorySearch.from_texts(
#                     # narrative_retrieval_list,
#                     narrating_dic["initial narrative stage"]["retrieval"],
#                     embedding=OpenAIEmbeddings(),
#                     )   
        
#         retriever = vectorstore.as_retriever()
        
        
#         contextualize_q_prompt = ChatPromptTemplate.from_messages(
#                     [
#                     ("system", contextualize_q_system_prompt),
#                     MessagesPlaceholder(variable_name="chat_history"),
#                     ("human", "{question}"),
#                     ]
#                 )
#         contextualize_q_chain = contextualize_q_prompt | model | StrOutputParser()

#         prompt = ChatPromptTemplate.from_messages(
#                     [
#                     ("system", narrating_dic["initial narrative stage"]["systemprompt"]),
#                     MessagesPlaceholder(variable_name="chat_history"),
#                     ("human", "{question}"),
#                     ]
#                 )


#         def contextualized_question(input: dict):
#                     if input.get("chat_history"):
#                         return contextualize_q_chain
#                     else:
#                         return input["question"]
                    
#         setup_and_retrieval = RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
#         setup_and_retrieval.add_item(input_variables_list[0], RunnablePassthrough())

#         rag_chain = (
#                     RunnablePassthrough.assign(
#                     context=contextualized_question | retriever 
#                 )
#                     | prompt
#                     | model
#                 )
        

#         invoke_dict = {"question": player_input, "chat_history": chat_history}
#         #invoke_dict[input_variables_list[0]] =  external_input # 添加新的键值对
                
           
#         ai_msg = rag_chain.invoke(invoke_dict)
#         chat_history.extend([HumanMessage(content=player_input), AIMessage(content=ai_msg.content)])
#         print("narrative:", ai_msg.content)
#                 #print if check the chat history
#                 #print("chat history:", chat_history)
        








@app.route('/reset', methods=['POST'])
def reset():
    global worldsetting_list
    global character_list
    global input_variables_list 
    global input_variables_demonstration
    global narrator_behavior_list
    worldsetting_list = []
    character_list = []
    input_variables_list = []
    input_variables_demonstration = []
    narrator_behavior_list = []
    return jsonify({'output': ''})
    
if __name__ == '__main__':
    app.run(debug=True)
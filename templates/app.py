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
narrative_retrieval_list = []
character_list = []
narrator_behavior_list = []

variable_dic = {}

#for page2 card creation
narrative_retrieval_list_no = 0
character_list_no = 0
narrator_behavior_list_no = 0
input_variables_list_no = 0

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
playerinput=""



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




# @app.route('/branching', methods=['POST', 'GET'])
# #@app.route('/world', methods=['POST'])
# #@app.route('/world')
# def system():
#     global narrative_retrieval_list
#     input_data = request.json
#     if input_data['id'] == 1:
#         branching i = //这里应该是卡片对应的~
#         narrative_retrieval_list.append(input_data['text'])
#         print(narrative_retrieval_list)  # Printing the result on the server console
    
#     return jsonify({'output': ''})



@app.route('/process')
#@app.route('/process', methods=['POST'])
def process():
    global narrative_retrieval_list
    global character_list
    global input_variables_list 
    global input_variables_demonstration
    global variable_dic
    input_data = request.json
    narrator.messages = [{"role": "assistant", "content": narrator.assistant_msg},
                         {"role": "user", "content": input_data['text']},
                        {"role": "system", "content": ' '.join(narrative_retrieval_list)+' '.join(character_list) }]
    print(' '.join(narrative_retrieval_list)+" " + ' '.join(character_list))
    narrator_response = narrator.get_completion()
    # Process the input data and generate output
    output_data = 'narrator: ' + narrator_response
    print(output_data)  # Printing the result on the server console
    # Send the result to the client-side JavaScript as a JSON response
    return jsonify({'output': output_data})






@app.route('/world', methods=['POST', 'GET'])
def system():
    global narrative_retrieval_list
    global character_list
    global input_variables_list 
    global input_variables_demonstration
    global variable_dic

    global narrator_behavior_list
    global newkey

    input_data = request.json
    if input_data['id'] == 1:
        narrative_retrieval_list.append(input_data['text'])
        print(narrative_retrieval_list)  # Printing the result on the server console
        
    elif input_data['id'] == 2:
        character_list.append(input_data['text'])
        print(character_list)  

    elif input_data['id'] == 5:
        narrator_behavior_list.append(input_data['text'])
        print(narrator_behavior_list)  
    

    #create a dictionary to store the variable and description
    elif input_data['id'] == 3:
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
    global narrative_retrieval_list
    global character_list
    global input_variables_list 
    global input_variables_demonstration
    global variable_dic
    global narrator_behavior_list

    data = request.json
    # if data['id'] == 1:
    #     narrative_retrieval_list.remove(data['value'])
    #     print(narrative_retrieval_list)  # Printing the result on the server console

    if data['id'] == 1:
     if data['value'] in narrative_retrieval_list:
        narrative_retrieval_list.remove(data['value'])
        print(narrative_retrieval_list)
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
    global narrative_retrieval_list
    global narrative_retrieval_list_no
    narrative_retrieval_list_no = len(narrative_retrieval_list)
    print("wordcardno", narrative_retrieval_list_no)
    data = {'value': narrative_retrieval_list_no, 'worldlist': narrative_retrieval_list}
    return jsonify(data)


@app.route('/charactercard')
def get_data2():
    global character_list
    global character_list_no
    character_list_no = len(character_list)
    print("charactercardno", character_list_no)
    data = {'value': character_list_no, 'characterlist': character_list}
    return jsonify(data)


@app.route('/narratorcard')
def get_data3():
    global narrator_behavior_list
    global narrator_behavior_list_no
    narrator_behavior_list_no = len(narrator_behavior_list)
    print("narratorno", narrator_behavior_list_no)
    data = {'value': narrator_behavior_list_no, 'narratorlist': narrator_behavior_list}
    return jsonify(data)

@app.route('/inputcard')
def get_data4():
    global variable_dic
    global input_variables_list_no
    global input_variables_demonstration
    input_variables_list_no = len(variable_dic)
    print("inputno", input_variables_list_no)
    data = {'value': input_variables_list_no, 'inputlist': input_variables_demonstration}
    return jsonify(data)




@app.route('/reset', methods=['POST'])
def reset():
    global narrative_retrieval_list
    global character_list
    global input_variables_list 
    global input_variables_demonstration
    global narrator_behavior_list
    narrative_retrieval_list = []
    character_list = []
    input_variables_list = []
    input_variables_demonstration = []
    narrator_behavior_list = []
    return jsonify({'output': ''})
    
if __name__ == '__main__':
    app.run(debug=True)
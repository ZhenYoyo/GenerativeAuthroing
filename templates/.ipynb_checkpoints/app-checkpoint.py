from flask import Flask, render_template, request, jsonify
import openai

#currently we can apply our own key, but later need to public this to let user to put their own key
openai.api_key = "sk-f29A4tQuVfHMbdcgqHrNIF3QRVJmbpnrqucE7V7062r4fz8L"
openai.api_base = "https://api.f2gpt.com/v1"

narrative_retrieval_list = []
narrator_behavior_list = []

playerinput=""


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

@app.route('/process', methods=['POST'])
def process():
    global narrative_retrieval_list
    global narrator_behavior_list
    global playerinput
    input_data = request.json
    narrator.messages = [{"role": "assistant", "content": narrator.assistant_msg},
                         {"role": "user", "content": input_data['text']},
                        {"role": "system", "content": ' '.join(narrative_retrieval_list)+' '.join(narrator_behavior_list) }]
    print(' '.join(narrative_retrieval_list)+" " + ' '.join(narrator_behavior_list))
    narrator_response = narrator.get_completion()
    # Process the input data and generate output
    output_data = 'narrator: ' + narrator_response
    print(output_data)  # Printing the result on the server console
    # Send the result to the client-side JavaScript as a JSON response
    return jsonify({'output': output_data})

@app.route('/world', methods=['POST'])
def system():
    global narrative_retrieval_list
    global narrator_behavior_list
    input_data = request.json
    if input_data['id'] == 1:
        narrative_retrieval_list.append(input_data['text'])
        print(narrative_retrieval_list)  # Printing the result on the server console
        
    elif input_data['id'] == 2:
        narrator_behavior_list.append(input_data['text'])
        print(narrator_behavior_list)  # Printing the result on the server console
    # Process the input data and generate output
    # Send the result to the client-side JavaScript as a JSON response
    return jsonify({'output': ''})
@app.route('/removeworld', methods=['POST'])
def removesystem():
    global narrative_retrieval_list
    global narrator_behavior_list
    data = request.json
    if data['id'] == 1:
        narrative_retrieval_list.remove(data['value'])
        print(narrative_retrieval_list)  # Printing the result on the server console
        
    elif data['id'] == 2:
        narrator_behavior_list.remove(data['value'])
        print(narrator_behavior_list)  # Printing the result on the server console
        
    # Send the result to the client-side JavaScript as a JSON response
    return jsonify({'output': ''})
@app.route('/reset', methods=['POST'])
def reset():
    global narrative_retrieval_list
    global narrator_behavior_list
    narrative_retrieval_list = []
    narrator_behavior_list = []
    return jsonify({'output': ''})
    
if __name__ == '__main__':
    app.run(debug=True)
import openai
import msvcrt

#currently we can apply our own key, but later need to public this to let user to put their own key
openai.api_key = "sk-f29A4tQuVfHMbdcgqHrNIF3QRVJmbpnrqucE7V7062r4fz8L"
openai.api_base = "https://api.f2gpt.com/v1"

narratorsystemprompt= ""
narratorsystempromptlist = []

narratoruserprompt=""
narratoruserpromptlist=[]



# a list?

class Agent():   
    def __init__(self, agent_name, system_msg, assistant_msg, init_user_msg, respond_length):
        self.agent_name = agent_name
        self.system_msg = system_msg
        self.assistant_msg = assistant_msg
        self.init_user_msg = init_user_msg
        self.respond_length = respond_length
        self.messages = [{"role": "system", "content": system_msg},
                         {"role": "assistant", "content": assistant_msg},
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


#need to test directly modify the agent's system prompt or wake up a new agent
narrator = Agent("narrator", 
                  narratorsystemprompt,
                  "Hi, I'm the narrator.", 
                  "", 
                  "30")





while True:
    # 监听用户输入
    user_input = input("<+ ")
    
    # 如果用户输入为空，则跳过
    if not user_input:
        continue
    
    if user_input.startswith("#systemprompt>"):
     narratorsystempromptlist.append(user_input[14:])
     print(narratorsystempromptlist)


    if user_input.startswith("#userprompt>"):
     narratoruserpromptlist.append(user_input[12:])
     print(narratoruserpromptlist)


    if user_input.startswith("#start"):
     systempromptindex = user_input[6:]
     #userpromptindex = user_input[7:]
     if systempromptindex.isdigit() and int(systempromptindex) < len(narratorsystempromptlist):
     #and userpromptindex() and int(userpromptindex) < len(narratoruserpromptlist):
    #  if int(systempromptindex) < len(narratorsystempromptlist) and int(userpromptindex) < len(narratoruserpromptlist):
        narratorsystemprompt = narratorsystempromptlist[int(systempromptindex)]
        print("systempromptnow:", narratorsystemprompt, "\n")
        #narratoruserprompt = narratoruserpromptlist[int(userpromptindex)]
        narrator.debug_mode = False
        narrator.messages.append({"role": "system", "content": narratorsystemprompt})
        narrator.messages.append({"role": "user", "content": "Hi the creature, tell me your story"})
        #narrator.messages.append({"role": "user", "content": narratoruserprompt})
        narrator_response = narrator.get_completion()
        print("narrator:", narrator_response, "\n")
     else:
        print("Invalid index!")

    if user_input == "DEBUG":
        narrator.debug_mode = True
        narrator_response = narrator.get_completion()
        print("\n narratorhistory:")
        print(narrator_response)
        narrator.debug_mode = False


import openai

#currently we can apply our own key, but later need to public this to let user to put their own key
openai.api_key = "sk-f29A4tQuVfHMbdcgqHrNIF3QRVJmbpnrqucE7V7062r4fz8L"
openai.api_base = "https://api.f2gpt.com/v1"

narratorsystemprompt= ""
narratorsystempromptlist = []

narratorsensorprompt=""
narratorsensorpromptlist=[]

#this is for simulating the real text input from the player(not the user-author of the interactive narrative) . if the player input is empty, then the system will proceed through "a viewing lense"
playerinput=""


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
    # listening to user input
    user_input = input("<+ ")
    
    # skip if no real input
    if not user_input:
        continue

#---FOR USER/AUTHOR. initial set up--define different system prompt and user prompt    
    if user_input.startswith("#systemprompt>"):
     narratorsystempromptlist.append(user_input[14:])
     print(narratorsystempromptlist)


    if user_input.startswith("#sensorprompt>"):
     narratorsensorpromptlist.append(user_input[12:])
     print(narratorsensorpromptlist)

#---FOR PLAYER. for control live play,
    #here is simulating the function of switching between different system prompt based on the narrative branching 
    #later should replace the text input method with the real condition
    if user_input.startswith("#switching"):
        systempromptindex = user_input[10:]
        if systempromptindex.isdigit() and int(systempromptindex) < len(narratorsystempromptlist):
            narratorsystemprompt = narratorsystempromptlist[int(systempromptindex)]
            print("currentsystemprompt:", narratorsystemprompt, "\n")

    #here is simulating the input from the real player
    if user_input.startswith("#playertext>"):
        playerinput = user_input[12:]
        print("currentplayerinput:", playerinput, "\n")

    #here is the conversation monitor
    if user_input.startswith("#start"):
     sensorpromptindex = user_input[6:]
     if sensorpromptindex.isdigit() and int(sensorpromptindex) < len(narratorsensorpromptlist):
        narratorsensorprompt = narratorsensorpromptlist[int(sensorpromptindex)]
        print("currentsensorprompt:", narratorsensorprompt, "\n")
        narrator.debug_mode = False
        narrator.messages.append({"role": "system", "content": narratorsystemprompt})
        narrator.messages.append({"role": "user", "content": narratorsensorprompt + playerinput})
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


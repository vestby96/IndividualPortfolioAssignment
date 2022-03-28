import socket
import threading
import random

# defining global constants, using commandline input
print("Enter IP")
IP = input('')
print("Enter PORT")
PORT = int(input())
ADDR = (IP, PORT)
print(f"ADDR: {ADDR}")

# you have to choose a bot that the client will use to respond to the host
while True:
    print("Choose a bot: 1. Joakim, 2. Vetle, 3. Sofie, 4. Erlend")
    msg = input()
    if "1" in msg or "Joakim" in msg:
        name = "Joakim"
        break
    elif "2" in msg or "Vetle" in msg:
        name = "Vetle"
        break
    elif "3" in msg or "Sofie" in msg:
        name = "Sofie"
        break
    elif "4" in msg or "Erlend" in msg:
        name = "Erlend"
        break

# buffersize used to receive messages, encryption used to both send and receive messages
BUFF = 1024
ENC = 'utf-8'

# creating the socket and connecting it with the address
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(ADDR)
except:
    print("Connection failed")

#--------------------------------------------------------------------------------------------------------------------
# start of the bot-script
# the bot function contains 4 bots with set responses

# list with actions that have already been suggested
used_actions = []

def bot(msg):
    # bot 1
    if name == "Joakim":
        # set lists og actions that the bot want and don't want to do
        # very easy to just add more actions in these lists to get the bot to respond to more
        yes_things = ["sing", "hug", "play", "work"]
        no_things = ["fight", "bicker", "yell", "complain", "cry"]

        # extracting the suggested action from the received message in the form of a list
        yes_action = [string for string in yes_things if string in msg]
        no_action = [string for string in no_things if string in msg]
        
        # the suggested action is in the yes_things list
        if yes_action:
            # the action has been suggested before
            if yes_action[0] in used_actions:
                return "yes, i told you that"
            
            # action is added to the use_action list
            used_actions.append(yes_action[0])
            return f"I'm down for some {yes_action[0]}ing."
        
        # the action is in no_things list
        elif no_action:
            if no_action[0] in used_actions:
                return "No, you already asked that"
            used_actions.append(no_action[0])
            return f"What? I don't want to {no_action[0]}."
        
        # does not find any action
        return "I don't care!"

    # bot 2
    elif name == "Vetle":
        # this bot has a different ide of want is fun
        yes_things = ["fight", "bicker", "yell", "complain", "cry"]
        no_things = ["sing", "hug", "play", "work", "run", "sing", "talk"]
        yes_action = [string for string in yes_things if string in msg]
        no_action = [string for string in no_things if string in msg]

        if yes_action:
            if yes_action[0] in used_actions:
                return "Still yes"
            used_actions.append(yes_action[0])
            return f"Yes! Time for {yes_action[0]}ing."
        elif no_action:
            if no_action[0] in used_actions:
                return "Not really, no"
            used_actions.append(no_action[0])
            return f"Not sure about {no_action[0]}ing."
        return "I don't care."

    # bot 3
    elif name == "Sofie":
        yes_things = ["sing", "hug", "play", "work"]
        no_things = ["fight", "bicker", "yell", "complain"]
        yes_action = [string for string in yes_things if string in msg]
        no_action = [string for string in no_things if string in msg]

        if yes_action:
            if yes_action[0] in used_actions:
                return "I'm too tired..."
            used_actions.append(yes_action[0])
            return f"Nah, that's exsausting."
        elif no_action:
            if no_action[0] in used_actions:
                return "Sigh, I sead no"
            # this bot can reply with a suggestion
            used_actions.append(no_action[0])
            suggestion = random.choice(yes_things)
            return f"That no fun, what about {suggestion}ing?"
        return "I don't care."
        
    # bot 4
    else:
        things = ["sing", "hug", "play", "work", "fight", "bicker", "yell", "complain", "sing", "code", ]
        action = [string for string in things if string in msg]        

        # this bot agrees to any action it recognizes
        if action:
            if action[0] in used_actions:
                return "Yes! I thought i made that clear"
            used_actions.append(action[0])
            return f"I think {action[0]}ing sounds great!"
        return "That sounds good."
#--------------------------------------------------------------------------------------------------------------------

# function that sends input, mainly used to disconnect clients
def send():
    while True:
        try:
            msg = f"{name} : {input()}"

            # the loop and thread will break when the disconnect message is sent
            if msg == f"{name} : quit":
                s.send(msg.encode(ENC))
                break
            else:
                s.send(msg.encode(ENC))
        except:
            # an error occured and the function can't send a message
            print("ERROR: Can't send")
            s.close()
            break

# function that looks for received messages through the socket
def rece():
    while True:
        try:
            msg = s.recv(BUFF).decode(ENC)

            # checks for the disconnect message
            if msg == "quit": 
                s.close()
                break

            # checks if the server is asking for your name
            elif msg == "NAME?": 
                s.send(name.encode(ENC))

            # checks if the message is from the host/server, and uses the bot to create a response
            elif "HOST : " in msg: 
                print(msg)
                message = bot(msg)
                if message:
                    print(message)
                    s.send(f"{name} : {message}".encode(ENC))
            
            # if the message is from one of the other clients/bots, the message will only be printed
            else: 
                print(msg)

        except:
            # exception if the connection is broken
            print("ERROR: Disconnect")
            s.close()
            break

# starting the send function as a thread so it can run uninterrupted from the rest of the script
th1 = threading.Thread(target=send)
th1.start()

# starting the rece function as a thread so it can run uninterrupted from the rest of the script
th2 = threading.Thread(target=rece)
th2.start()
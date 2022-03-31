import datetime
import socket
import threading
import random
import argparse

# -h description
parser=argparse.ArgumentParser(
    description="Server IP address and port is chosen by the user when the server is launched. The script will ask you to enter IP, Port and which bot the script will use. The client.py script will take commandline input and send to all other clients like a chatroom, but the bot will only respond if the message is from the host. Commands: '/names' will list all connected clients with name, '/quit' will close the connection with the server")
args=parser.parse_args()

# defining global constants, using commandline input
print("Enter IP of the server")
IP = input('')
print("Enter Port")
PORT = int(input())
ADDR = (IP, PORT)
print(f"ADDR: {ADDR}")

# buffersize used to receive messages, encryption used to both send and receive messages
BUFF = 1024
ENC = 'utf-8'

# creating the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# all connected client names will be stored here
names = []

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

# connecting to the server through the address entered
try:
    s.connect(ADDR)
except:
    print("Error: No connection")

#--------------------------------------------------------------------------------------------------------------------
# start of the bot
# the bot function contains 4 bots with set responses
# the bots all work pretty much the same, just with different reponses

# list of actions that have already been suggested
used_actions = []

#-----------------------------------------------------------------------------------------------
def bot(msg):
    # bot 1 Joakim
    if name == "Joakim":
        # set lists og actions that the bot want and don't want to do
        # very easy to just add more actions in these lists if you want the bot to respond to more
        yes_things = ["sing", "hug", "play", "work", "eat", "day is it today", "spare time"]
        no_things = ["fight", "bicker", "yell", "complain", "cry"]

        # extracting the suggested action from the received message in the form of a list
        yes_action = [string for string in yes_things if string in msg]
        no_action = [string for string in no_things if string in msg]
        
        # host will always initiate a new round of dialog
        if msg.startswith("HOST:"):        

            # the suggested action is in the yes_things list
            if yes_action:

                # special responses for some questions
                if "day is it today" in yes_action:
                    day = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                    today = day[datetime.datetime.today().weekday()]
                    return f"Today is {today}"
                
                elif "spare time" in yes_action:
                    things = ["sing", "hug", "play", "work", "eat"]
                    suggestion = random.choice(things)
                    return f"I like to {suggestion} in my spare time"

                elif "eat" in yes_action:
                    return "I'm starving for some tacos"

                # the action has been suggested before
                elif yes_action[0] in used_actions:
                    return "Yes, i told you that"
                
                # the action has not been suggested before and will be added to the used_actions list
                used_actions.append(yes_action[0])
                # returns a response
                return f"I'm down for some {yes_action[0]}ing."
            
            # the action is in no_things list
            elif no_action:
                if no_action[0] in used_actions:
                    return "No, you already asked that"
                used_actions.append(no_action[0])
                return f"What? I don't want to {no_action[0]}."
            
            # does not find any action in the hosts message
            return "I don't care!"
#-----------------------------------------------------------------------------------------------
    # bot 2 Vetle, this bot has a different idea of want is fun
    elif name == "Vetle":

        yes_things = ["fight", "bicker", "yell", "complain", "cry", "eat", "spare time", "day is it today"]
        no_things = ["sing", "hug", "play", "work", "run", "sing", "talk"]
        yes_action = [string for string in yes_things if string in msg]
        no_action = [string for string in no_things if string in msg]

        if msg.startswith("HOST:"):

            if yes_action:

                if "day is it today" in yes_action:
                    day = ["thursday", "friday", "saturday", "sunday", "monday", "tuesday", "wednesday"]
                    today = day[datetime.datetime.today().weekday()]
                    return f"Well today is {today}, of course!"
                
                elif "spare time" in yes_action:
                    things = ["fight", "bicker", "yell", "complain", "cry"]
                    suggestion = random.choice(things)
                    return f"I'm into {suggestion}ing"

                elif "eat" in yes_action:
                    return f"Hmm, ok i could eat"

                elif yes_action[0] in used_actions:
                    return "You already said that..."
                
                used_actions.append(yes_action[0])
                return f"Yes! Time for {yes_action[0]}ing."
            
            elif no_action:
                if no_action[0] in used_actions:
                    return "Not really, no"
                used_actions.append(no_action[0])
                return f"Not sure about {no_action[0]}ing."
            
            return "I don't care!"

#-----------------------------------------------------------------------------------------------
    # bot 3
    if name == "Sofie":
        yes_things = ["relax", "sleep", "code", "day is it today", "spare time", "eat"]
        no_things = ["fight", "bicker", "yell", "complain", "work", "jogg"]
        
        yes_action = [string for string in yes_things if string in msg]
        no_action = [string for string in no_things if string in msg]
        
        if msg.startswith("HOST:"):        

            if yes_action:

                if "day is it today" in yes_action:
                    return "I don't actually care..."
                
                elif "spare time" in yes_action:
                    things = ["relax", "watch TV", "play video games"]
                    suggestion = random.choice(things)
                    return f"I like to {suggestion} in my spare time"

                elif "eat" in yes_action:
                    return "I would like some soup"

                elif yes_action[0] in used_actions:
                    return "Sure"
                
                used_actions.append(yes_action[0])
                return f"OK, {yes_action[0]}ing sounds fun"
            
            elif no_action:
                if no_action[0] in used_actions:
                    return "Sigh, I said no"
                used_actions.append(no_action[0])
                things = ["relax", "watch TV", "play video games"]
                suggestion = random.choice(things)
                return f"That's no fun, what if we {suggestion}?"
            
            return "I don't care!"
#-----------------------------------------------------------------------------------------------
    # bot 4, this bot positive to everything
    elif name == "Erlend":
        things = ["sing", "hug", "play", "work", "fight", "bicker", "yell", "complain", "sing", "code", "day is it today", "spare time", "eat"]
        action = [string for string in things if string in msg]

        if msg.startswith("HOST:"):
            if action:
                if "day is it today" in action:
                    return "Oh, wish i knew"
                
                elif "spare time" in action:
                    return f"I like to do anything really"

                elif "eat" in action:
                    return "I could go for anything!"

                elif action[0] in used_actions:
                    return f"{action[0]}ing is alot of fun!"
                used_actions.append(action[0])
                return f"Yeah, {action[0]}ing sounds fun"

            return "Not sure what you mean"
            
#--------------------------------------------------------------------------------------------------------------------

# function that sends input, mainly used to disconnect clients
def send():
    while True:
        try:
            # looks for input
            msg = f"{name}: {input()}"

            # the loop will break when the disconnect message is sent
            if msg == f"{name}: /quit":
                s.send(msg.encode(ENC))
                break

            # the /names command prints the names list
            elif msg == f"{name}: /names":
                print(names)
            
            # sends the input message
            else:
                s.send(msg.encode(ENC))
        
        except:
            # an error occured and the function can't send a message
            print("ERROR: send()")
            s.close()
            break

# function that looks for received messages through the socket
def rece():
    while True:
        try:
            # looks for receieved data
            msg = s.recv(BUFF).decode(ENC)
            
            # checks if the server is asking for your name
            if msg == "NAME?":
                # send name
                s.send(name.encode(ENC))
                # receives a string of a list, that is that copied to the names list
                message = s.recv(BUFF).decode(ENC)
                message = message[2:-2]
                strlist = list(message.split("', '"))
                for n in strlist:
                    names.append(n)
                # prints all connected clients
                print(f"Connected users: {names}")
            
            # if a new cilent has connected to the server
            elif msg.startswith("[NEWNAME]"):
                # adds the name to the names list
                names.append(msg[10:])
                # prints the name
                print(f"{msg[10:]} HAS JOINED THE CHAT")

            # if a client disconnects
            elif msg.startswith("[DISCONNECTED]"):
                # removes the name from the names list
                names.remove(msg[15:])
                # prints the message
                print(msg)
            
            # checks for the disconnect message
            elif msg == "/quit": 
                break

            else:
                print(msg)
                # calls the bot for a response
                message = bot(msg)
                # prints and sends the bots response if there is one
                if message:
                    print(message)
                    s.send(f"{name}: {message}".encode(ENC))
        except:
            # exception if the connection is broken
            print("ERROR: rece()")
            s.close()
            break

# starting the send function as a thread so it can run uninterrupted from the rest of the script
th1 = threading.Thread(target=send)
th1.start()

# starting the rece function as a thread so it can run uninterrupted from the rest of the script
th2 = threading.Thread(target=rece)
th2.start()  
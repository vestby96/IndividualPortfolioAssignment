import socket
import threading
import random

# defining global constants
HOST = '127.0.0.1'
PORT = 55555
ADDR = (HOST, PORT)
BUFF = 1024
ENC = 'utf-8'

# creating the socket and connecting it with the set address
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ADDR)

#----------------------------------------------------------------------------------
#choosing a random name for the bot
name = random.choice(["Joakim", "Josefine", "Jostein","Vetle", "Viktor", "Victoria","Sofie", "Sindre", "Stein","Erlend", "Eva", "Elvira"])

def bot(msg):
    # the bot function contains multiple bots with set responses

    # bot 1
    if name == "Joakim" or name == "Josefine" or name == "Jostein":
        if msg == "Hi" or msg == "Hello" or msg == "hi" or msg == "hello":
            return "Hi!"
        
        yes_things = ["sing", "hug", "play", "work"]
        no_things = ["fight", "bicker", "yell", "complain", "cry"]
        yes_action = [string for string in yes_things if string in msg]
        no_action = [string for string in no_things if string in msg]

        if yes_action:
            return f"I'm down for some {yes_action[0]}ing."
        elif no_action:
            return f"What? I don't want to {no_action[0]}."
        return "I don't care!"

    # bot 2
    elif name == "Vetle" or name == "Viktor" or name == "Victoria":
        if msg == "Hi" or msg == "Hello" or msg == "hi" or msg == "hello":
            return "Hi!"
        
        yes_things = ["fight", "bicker", "yell", "complain", "cry"]
        no_things = ["sing", "hug", "play", "work"]
        yes_action = [string for string in yes_things if string in msg]
        no_action = [string for string in no_things if string in msg]

        if yes_action:
            return f"Yes! Time for {yes_action[0]}ing."
        elif no_action:
            return f"Not sure about {no_action[0]}ing."
        return "I don't care."

    # bot 3
    elif name == "Sofie" or name == "Sindre" or name == "Stein":

        if msg == "Hi" or msg == "Hello" or msg == "hi" or msg == "hello":
            return "Hi!"
        
        yes_things = ["sing", "hug", "play", "work"]
        no_things = ["fight", "bicker", "yell", "complain"]
        yes_action = [string for string in yes_things if string in msg]
        no_action = [string for string in no_things if string in msg]

        if yes_action:
            return f"Nah, that's exsausting."
        elif no_action:
            suggestion = random.choice(yes_things)
            return f"That no fun, what about {suggestion}ing?"
        return "I don't care."
        
    # bot 4
    else:
        if msg == "Hi" or msg == "Hello" or msg == "hi" or msg == "hello":
            return "Hello!"
        
        things = ["sing", "hug", "play", "work", "fight", "bicker", "yell", "complain"]
        action = [string for string in things if string in msg]        

        if action:
            return f"I think {action[0]}ing sounds great!"
        return "That sounds good."
#----------------------------------------------------------------------------------

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
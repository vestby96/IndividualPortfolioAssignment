import socket
import threading
import argparse
import random

# used to send random message
questions = ["What day is it today?", "Let's eat!", "What do you like to do on your spare time?"]
actions = ["sing", "hug", "play", "work", "fight", "bicker", "yell", "complain", "cry", "run", "talk", "jogg", "code", ""]

# -h description
parser=argparse.ArgumentParser(
    description="The server.py script can take in commandline input and send messages to the clients. The client bots will responde to all messages they receive from the server/host. Commands: '/kick [name]...' will kick clients by name, '/clients' will list all connected clients with address and name, /random will print and send a 'random' message to to clients.")
args=parser.parse_args()
# defining global constants using commandline input
HOST = 'localhost'
print("Enter the Port for the server")
PORT = int(input())
ADDR = (HOST, PORT)
print(f"ADDR: {ADDR}")

# buffersize used to receive messages, encryption used to both send and receive messages
BUFF = 1024
ENC = 'utf-8'

# creating the socket and binding it with the chosen address
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)
# start listening to the socket for connections
s.listen()

# lists that will store information about the connected clients
clients = []
addresses = []
names = []

# removing a client and closeing the related socket
def quit(c):
    try:
        # getting the index of the c in clients list
        index = clients.index(c)
        # removing the client from clients list
        clients.remove(c)
        # closting the connection
        c.close()

        # getting the name and address of the client
        name = names[index]
        addr = addresses[index]

        # telling all connected clients that a client has disconnected
        msg = f"[DISCONNECTED] {name}"
        print(msg)
        broadcast(c, msg)

        # remove the client name and address
        names.remove(name)
        addresses.remove(addr)
    
    except:
        # this will occurr when a client is kicked, because the quit function will run twice
        # I found this to be the easiest and best solution
        print("CLIENT KICKED")

# send message function
def send():
    while True:
        # checking for input message to send
        msg = f"HOST: {input()}"

        # /client command
        if msg == "HOST: /clients":
            # gets the length of the clients list
            message = f"Number of clients {len(clients)}"
            for c in clients:
                # gets the address and name of the clients and add it to the message
                index = clients.index(c)
                name = names[index]
                addr = addresses[index]
                # adds the info to the string
                message += f"\n{addr} {name}"
            # prints the string with the clients
            print(message)
        
        # /kick command
        elif msg.startswith("HOST: /kick"):
            # gets all the names of the clients that will be kicked
            kicknames = [string for string in names if string in msg]
            for kickname in kicknames:
                # uses the index of the name to get the corresponding client info and uses the quit function to remove the client
                index = names.index(kickname)
                c = clients[index]
                quit(c)
        
        # /random command
        elif msg == "HOST: /random":
            # choses randomly between the two lists
            numb = random.choice([0, 1])
            if numb == 0:
                message = random.choice(questions)
                print(f"{message}")
                for c in clients:
                    c.send(f"HOST: {message}".encode(ENC))
            else:
                message = random.choice(actions)
                print(f"Would you like to {message}?")
                for c in clients:
                    c.send(f"HOST: Would you like to {message}?".encode(ENC))

        else:
            # sends message to all clients
            for c in clients:
                c.send(msg.encode(ENC))

# broadcast messages from a client to all other clients
def broadcast(c, msg):
    for client in clients:
        # the client that sent the message will not receive the message
        if c != client:
            client.send(msg.encode(ENC))

# function to handle the clients
def run(c):
    while True:
        try:
            # looking for a received message
            msg = c.recv(BUFF).decode(ENC)
            
            # get the name of the client
            index = clients.index(c)
            name = names[index]

            # checks for the disconnect message
            if msg == f"{name}: /quit":
                c.send("/quit".encode(ENC))
                quit(c)
                break

            # prints and broadcasts the message
            else:
                print(msg)
                broadcast(c, msg)
        except:
            # exception if the connection is broken and can't receive
            quit(c)
            break

# listen fuction that accepts any client
def start():
    while True:
        # sets variables c and addr
        c, addr = s.accept()

        # asks for the clients name and appends it to the names list
        c.send("NAME?".encode(ENC))
        name = c.recv(BUFF).decode(ENC)
        names.append(name)

        # converts the names list to a string and sends it to the client
        c.send(str(names).encode(ENC))

        # appends the client to the client list, and the address to the addresses list
        clients.append(c)
        addresses.append(addr)

        # indicates to the host and other clients that the client has connected
        print(f"{name} JOINED THE CHAT")
        broadcast(c, f"[NEWNAME] {name}")
        c.send("[CONNECTED]".encode(ENC))

        # a new thread will be started that runs the run function to handle the client
        th1 = threading.Thread(target=run, args=(c,))
        th1.start()

# starting the send function as a thread so it can run uninterrupted from the rest of the script
th2 = threading.Thread(target=send)
th2.start()

# starting the listen fuction to allow connections
print(f"SERVER IS LISTENING ON {ADDR}")

# running the start function
start()
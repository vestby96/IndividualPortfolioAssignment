import socket
import threading

# defining global constants
HOST = '127.0.0.1'
PORT = 55555
ADDR = (HOST, PORT)
BUFF = 1024
ENC = 'utf-8'

# creating the socket and binding it with the set address
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)
# start listening to the socket for connections
# can add a number to the () if you want to limit the number of clients connected at once
s.listen()

# lists that wil store information about the connected clients
clients = []
addresses = []
names = []

# lists address and name of all connected clients
def listclients():
    # gets the length of the clients list
    msg = f"Number of clients: {len(clients)}"
    for c in clients:
        # gets the address and name of the clients and add it to the message
        index = clients.index(c)
        name = names[index]
        addr = addresses[index]
        msg += f"\n{addr} : {name}"
    return msg

# removing a client and close the related socket
def quit(c):
    try:
        index = clients.index(c)
        clients.remove(c)
        c.close()
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
        # i found this to be the easiest and best solution
        print("Client removed")

# HOST sends a message to all clients connected
def send():
    while True:
        # checking or input message to send
        msg = input()

        # i the message is the /client command
        if msg.startswith("/clients"):
            print(listclients())
        
        # /kick command
        elif msg.startswith("/kick"):
            kicknames = [string for string in names if string in msg]
            for kickname in kicknames:
                index = names.index(kickname)
                c = clients[index]
                quit(c)
        else:
            # sends message to all clients
            message = "HOST : " + msg
            for c in clients:
                c.send(message.encode(ENC))

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
            if msg == f"{name} : quit":
                c.send("quit".encode(ENC))
                quit(c)
                break

            # checks for the /clients command
            elif msg == f"{name} : /clients":
                c.send(listclients().encode(ENC))
            
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

        # appends the client to the client list, and the address to the addresses list
        clients.append(c)
        addresses.append(addr)

        # indicates to the host and other clients that the client has connected
        print(f"{name} JOINED")
        broadcast(c, f"{name} JOINED")
        c.send("[CONNECTED]\nTo see all clients type '/clients'".encode(ENC))

        # a new thread will be started that runs the run function to handle the client
        th1 = threading.Thread(target=run, args=(c,))
        th1.start()

# starting the send function as a thread so it can run uninterrupted from the rest of the script
th2 = threading.Thread(target=send)
th2.start()

# starting the listen fuction to allow connections
print("SERVER IS LISTENING...\nTo see all clients type '/clients'")
# running the start function
start()
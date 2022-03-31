Individual Portfolio Assignment

Erlend Søfting Vestby
s341950
Oslomet

Git hub repository:
https://github.com/vestby96/IndividualPortfolioAssignment.git


Introduction

As I interpret the task, I will create a server that allows any connections and lets the connected clients chat with each other. The client will connect to the server, given the right IP and Port. Then I shall create a client.py script that will connect to the server, and act as a bot. The server/host will send messages that the bot will react to. This will create rounds of dialog where the host sends a message, and receives responses from all the bots connected.

Bot

The bot function is only in the client.py script. It contains multiple bots, but only one will be used per client, and is chosen when connecting to the server. The bots will remember actions that have been previously suggested by storing it as a string in a list. If the action is in the list the bot will react differently.

The bot will only respond if the message is from the host. This is because the bots are made to only react to the action in the received message, which means they don’t know the difference between a response from another bot or a suggestion.
The bot takes in a single string and searches for an action in it. If it does not recognize any actions, the bot will respond with “I don’t care.” 

How to use

server.py

When first launching the server.py script it will ask for a port, which you must enter in the command line. Then the script will tell you which IP and port it is listening to. From this point, while the server is running, the clients can connect and disconnect as they choose. 
The server can take command line inputs as a command, or it can send messages to the clients. The ‘/kick’ command can be used to kick clients, the ‘/clients’ command will list all clients with names and addresses, and the ‘/random’ command will send a random message to the clients.

client.py

After running the client.py script it will ask you for an IP and a Port, which will be used to connect the socket with the server-socket. Then you must choose which bot-personality the client will take on, either enter the full name or just the number associated with the name. If there is an error connecting with the server it will close the script here, if not a message displaying ‘Connected’ will appear. If you get the error, please check the address that the server is listening on and try again.

When you are connected you can send and receive messages to and from the clients and the host. If a message is received from the host, the bot will automatically send a response. The bot will not react to messages received from other clients. There are two commands that the client can use, ‘/names’ will print the names of all connected clients, ‘/quit’ will disconnect you from the server.

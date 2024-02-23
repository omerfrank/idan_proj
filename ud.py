import socket
import select
import time
import re
server = socket.socket()
server.bind(('127.0.0.1', 1729))
server.listen()
clients = []
messages=[]
names = {}
while True:
    rlist, wlist, xlist = select.select([server]+clients, clients, [])
    for client in rlist:
        if client is server:
            print('new client')
            c, address = client.accept()
            clients.append(c)   
        else:
            msg=client.recv(1024).decode()
            if len(msg)>0:
                print(msg) 
                messages.append((client, "answer"))
                x = msg.split(":")
                x = x[0]
                if x not in names.keys():
                    names[x] = client
                    print(f"a wild '{x}' appeard!")
    for message in messages:
        x = msg.split(":")[0]
        client,msg = message
        if client in wlist:
            if x in names.keys():
                names[x].send(msg.encode())
            else:    
                client.send(msg.encode())
                client.send(names.keys().encode())
            messages.remove(message)

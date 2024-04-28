import socket
import select
import threading
import rsa
server = socket.socket()
server.bind(('127.0.0.1', 1729))
server.listen()
clients = []
messages=[]
def handleClients(client):
    pass
while True:
    rlist, wlist, xlist = select.select([server]+clients, clients, [])
    for client in rlist:
        if client is server:
            print('new client')
            c, address = client.accept()
            clients.append(c) 
            t = threading.Thread(target=handleClients(c))
            t.start()  


import socket
import select
import threading
import rsa
import pickle
import sqlite3
import time
server = socket.socket()
server.bind(('localhost', 1729))
server.listen()
clients = []
messages=[]
def handleClients(client):
    Keys = rsa.newkeys(1024)
    publicKey = Keys[0]
    privateKey = Keys[1]
    client = socket.socket()
    client.connect()
    client.send(f'{pickle.dumps(publicKey)}')
    url = rsa.decrypt(bytes(client.recv(1024),'utf-8') ,privateKey)
    while True:
        try:
           conn = sqlite3.connect(r'server side\\URL_database.db') 
           cursor = conn.cursor()
           cursor.execute
        except:
            time.sleep(0.2)
    
while True:
    rlist, wlist, xlist = select.select([server]+clients, clients, [])
    for client in rlist:
        if client is server:
            print('new client')
            c, address = client.accept()
            clients.append(c) 
            t = threading.Thread(target=handleClients,args=[c])
            t.start()  


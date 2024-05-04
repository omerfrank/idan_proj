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
def checkURL(url):
    injection_keywords = ['SELECT', 'UPDATE', 'DELETE', 'INSERT', '--', ';']
    for keyword in injection_keywords:
        if keyword.lower() in url.lower():
            return True
    return False
def handleClients(client):
    Keys = rsa.newkeys(1024)
    publicKey = Keys[0]
    privateKey = Keys[1]
    client = socket.socket()
    client.connect()
    client.send(f'{pickle.dumps(publicKey)}')
    url = rsa.decrypt(bytes(client.recv(1024),'utf-8') ,privateKey)
    if checkURL(url):
        return -1
    while True:
        try:
           conn = sqlite3.connect(r'server side\\URL_database.db') 
           cursor = conn.cursor()
           cursor.execute(f"SELECT isMal from Site where URL == '{url}'")
           try:
               response = cursor.fetchall[0][0]
               client.sendall(f'{response}'.encode())
           except:
               client.sendall('404 not found'.encode())
           client.close()
        except:
            time.sleep(0.2)

    
while True:
    rlist, wlist, xlist = select.select([server]+clients, clients, [])
    for client in rlist:
        if client is server:
            c, address = client.accept()
            if c.recv(1024).decode() == 'new':
                print('new client')
                c.close()
            else:
                t = threading.Thread(target=handleClients,args=[c])
                t.start()  


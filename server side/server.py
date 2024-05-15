import socket
import select
import threading
import rsa
import pickle
import sqlite3
import time
server = socket.socket()
print('server listening on port 1729')
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
    client.send(pickle.dumps(publicKey))
    print('sended publicKey \n')
    #url = rsa.decrypt(bytes(client.recv(2048),'utf-8') ,privateKey)
    url = rsa.decrypt(client.recv(2048) ,privateKey).decode()
    print(url + "\n")
    if checkURL(url):
        client.sendall('Mal')
        return 
    print("not sql injection \n")
    while True:
        try:
            conn = sqlite3.connect(r'server side\\URL_database.db') 
            print ("connected to DB \n")
            cursor = conn.cursor()
            cursor.execute(f"SELECT isMal from Site where URL == '{url}'")
            print('trying to fetch')
            response = cursor.fetchone()
            if response:
                response = response[0]
                print (response)
            else:
                client.send("".encode())
                client.close()
                return
            print(f"answer: {response}")
            client.sendall(f'{response}'.encode())
            print("sent answer")
            #client.sendall('404 not found'.encode())
            client.close()
            return
        except:
            time.sleep(0.2)

    
while True:
    rlist, wlist, xlist = select.select([server]+clients, clients, [])
    for client in rlist:
        if client is server:
            try:
                
                c, address = client.accept()
                print('connected to a client')
                if c.recv(1024).decode() == 'new':
                    print('new client')
                    c.close()
                else:
                    print("start a new thread")
                    t = threading.Thread(target=handleClients,args=[c])
                    t.start() 
            except:
                print('problem connecting')


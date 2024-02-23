import socket

client = socket.socket()
client.connect(('127.0.0.1', 1729))
while True:
    try:
        client.send(input("mes for server: ").encode())
        print((client.recv(1024).decode()))
    except:
        pass
client.close()

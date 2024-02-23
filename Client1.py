import socket
import  msvcrt
import  select
client = socket.socket()
client.connect(('127.0.0.1', 1729))
msg=""
while True:
    rlist,wlist,xlist = select.select([client],[client],[])
    for client in rlist:
        message = client.recv(1024).decode()
        if message != "":
            print(message)
    if msvcrt.kbhit():
        keypressed = msvcrt.getch().decode()
        print(keypressed,end="",flush=True)
        if keypressed == '\r' or keypressed == '\n':
            print(flush = True)
            client.send(msg.encode())
            msg = ''
        else:
            msg += keypressed
client.close()

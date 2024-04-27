import socket
import rsa
Keys = rsa.newkeys(1024)
#print (Keys)
publicKey = Keys[0]
messege = 'heloo warld'
x = rsa.encrypt(pub_key=publicKey, message= bytes(messege,'utf-8'))
print(rsa.decrypt(x,Keys[1]))
import socket
import rsa
import sqlite3
Keys = rsa.newkeys(1024)
#print (Keys)
publicKey = Keys[0]
messege = 'heloo warld'
x = rsa.encrypt(pub_key=publicKey, message= bytes(messege,'utf-8'))
#print(rsa.decrypt(x,Keys[1]))
conn = sqlite3.connect(r'C:\Users\omerf\OneDrive\שולחן העבודה\idan_proj\URL_database.db')
cursor = conn.cursor()
cursor.execute("SELECT isMal from Site where URL == 'drive.google.com'")
rows = cursor.fetchall()
print(rows[0][0])
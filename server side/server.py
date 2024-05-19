import socket
import select
import threading
import rsa
import pickle
import sqlite3
import time
import collections
def read_corpus(filename):
    print('try to poen')
    try:
        with open(r'server side\autoCorrect.txt', 'r') as f:
            print('opend suc')
            return f.read().lower()
    except:
            with open(r'autoCorrect.txt', 'r') as f:
                print('opend suc')
                return f.read().lower()
def get_word_counts(text):
    """Returns a dictionary where keys are unique words and values are their counts."""
    word_counts = collections.Counter(text.split())
    return word_counts

def edit_distance_1(word):
    """Generates all strings with 1 edit distance from the input word."""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    results = []

    # Add a character anywhere
    for i in range(len(word) + 1):
        for char in alphabet:
            new_word = word[:i] + char + word[i:]
            results.append(new_word)

    # Remove a character
    if len(word) > 1:
        for i in range(len(word)):
            new_word = word[:i] + word[i + 1:]
            results.append(new_word)

    # Transpose adjacent characters
    if len(word) > 1:
        for i in range(len(word) - 1):
            new_word = word[:i] + word[i + 1] + word[i] + word[i + 2:]
            results.append(new_word)

    # Substitute a character
    for i in range(len(word)):
        for char in alphabet:
            new_word = word[:i] + char + word[i + 1:]
            results.append(new_word)

    return results

def correct(word, word_counts):
    """Attempts to correct the spelling of a word."""
    if word in word_counts:
        return word

    max_count = 0
    correct_word = word
    edit_1_words = edit_distance_1(word)
    edit_2_words = []

    # Generate edit distance 2 words
    for edit_1_word in edit_1_words:
        edit_2_words.extend(edit_distance_1(edit_1_word))

    # Find the most frequent word within edit distance 1
    for edit_1_word in edit_1_words:
        if edit_1_word in word_counts and word_counts[edit_1_word] > max_count:
            max_count = word_counts[edit_1_word]
            correct_word = edit_1_word

    # Find the most frequent word within edit distance 2 (if length > 6)
    if len(word) > 6:
        max_count_2 = 0
        correct_word_2 = correct_word
        for edit_2_word in edit_2_words:
            if edit_2_word in word_counts and word_counts[edit_2_word] > max_count_2:
                max_count_2 = word_counts[edit_2_word]
                correct_word_2 = edit_2_word

        if max_count_2 > 4 * max_count:  # More lenient for longer words
            return correct_word_2

    return correct_word

def findCloseWords(input_words):
    """Reads the corpus, corrects user-provided words, and prints the results."""
    input_words = input_words.split()
    print("start to find")
    corpus_filename = r'\\autoCorrect.txt'
    corpus_text = read_corpus(corpus_filename)
    print("corpos")
    word_counts = get_word_counts(corpus_text)
    output = []

    for word in input_words:
        correction = correct(word.lower(), word_counts)
        if correction == word:
            output.append(f"- {word} is spelled correctly.")
        else:
            output.append(f"- {word} should be spelled as {correction}.")

    return "".join(output)

server = socket.socket()
print('server listening on port 1729')
server.bind((socket.gethostbyname(socket.gethostname()), 1729))
print("bound on: " + socket.gethostbyname(socket.gethostname()))
server.listen()
clients = []
messages=[]
def menangeServer():
    while True:
        requst = input("what do you want to add?")
        addToDb(site=requst)
        
        
def addToDb(site):
    if checkURL(site): 
        print ('Error inserting ' + site)
        return
    while True:
        try:
            conn = sqlite3.connect(r'server side\\URL_database.db') 
            print ("connected to DB \n")
            cursor = conn.cursor()
            Classification = input("Good or Mal? ")
            print(Classification)
            while (Classification != 'Good' and Classification !='Mal'):
                Classification = input("Good or Mal? ")
            print("passed while")
            insert_query = 'INSERT INTO Site(URL, IsMal) VALUES (?, ?)'
            cursor.execute(insert_query, (site, Classification))
            cursor.close()
            return
        except:
            time.sleep(0.2)
            
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
                client.send(findCloseWords(url).encode())
                client.close()
                return
            print(f"answer: {response}")
            if response == 'Good':
                client.sendall(f'{response}'.encode())
            else:
                client.sendall(f'{response}{findCloseWords(url)}'.encode())
            print("sent answer")
            #client.sendall('404 not found'.encode())
            client.close()
            return
        except:
            time.sleep(0.2)

# t = threading.Thread(target=menangeServer)
# t.start()
print("thread start")    
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


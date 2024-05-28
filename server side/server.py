import socket
import select
import threading
import rsa
import pickle
import sqlite3
import time
import collections
import numpy as np
import pickle
import requests
from urllib.parse import urlparse
import re
import ipaddress
import datetime
import whois

def get_domain(url):  
    domain = urlparse(url).netloc
    if re.match(r"^www.",domain):
        domain = domain.replace("www.","")
    return domain

def having_ip(url):
    try:
        ipaddress.ip_address(url)
        ip = 1
    except:
        ip = 0
    return ip

def have_at_sign(url):
    if "@" or '%40' in url:
        at = 1
    else:
        at = 0
    return at

def get_length(url):
    if len(f'https:{url}') < 54:
        length = 0
    else:
        length = 1
    return length

def get_depth(url):
    s = urlparse(url).path.split('/')
    depth = 0
    for j in range(len(s)):
        if len(s[j]) != 0:
            depth = depth+1
    return depth

def redirection(url):
    newrl = 'http://' + url if 'http:/' or 'https:/' not in url else url
    pos = newrl.rfind('//')
    if pos > 6:
        if pos > 7:
            return 1
        else:
            return 0
    else:
        return 0

def http_domain(url):
    domain = urlparse(url).netloc
    if 'https' in domain:
        return 1
    else:
        return 0

def tiny_url(url):
    shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                          r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                          r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                          r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                          r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                          r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                          r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                          r"tr\.im|link\.zip\.net"
    match=re.search(shortening_services,url)
    if match:
        return 1
    else:
        return 0

def prefix_suffix(url):
    if '-' in urlparse(url).netloc:
        return 1
    else:
        return 0 
def domainEnd(domain_name):
  expiration_date = domain_name.expiration_date
  if isinstance(expiration_date,str):
    try:
      expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
    except:
      print(1)
      return 1
  if (expiration_date is None):
      print(1)
      return 1
  elif (type(expiration_date) is list):
      print(1)
      return 1
  else:
    today = datetime.now()
    end = abs((expiration_date - today).days)
    if ((end/30) < 6):
      end = 0
    else:
      print(1)
      end = 1
  return end
# 13.Survival time of domain: The difference between termination time and creation time (Domain_Age)  
def domainAge(domain_name):
  creation_date = domain_name.creation_date
  expiration_date = domain_name.expiration_date
  if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
    try:
      creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
      expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
    except:
      print(1)
      return 1
  if ((expiration_date is None) or (creation_date is None)):
      print(1)
      return 1
  elif ((type(expiration_date) is list) or (type(creation_date) is list)):
      print(1)
      return 1
  else:
    ageofdomain = abs((expiration_date - creation_date).days)
    if ((ageofdomain/30) < 6):
      age = 1
    else:
      age = 0
  print(age)
  return age
def web_traffic(url):
    try:
        querystring = {"domain": get_domain(url)}
        headers = {
            "X-RapidAPI-Key": "cd4733fedbmsh6f2cfc21cf195f2p1d088djsn84e6c824c74e",
            "X-RapidAPI-Host": "similar-web.p.rapidapi.com"
        }
        response = requests.get("https://similar-web.p.rapidapi.com/get-analysis", headers=headers, params=querystring)
        data = response.json()
        rank = data['GlobalRank']['Rank']
        try:
            rank = int(rank)
        except:
            rank =1
    except (requests.exceptions.RequestException, ValueError, KeyError):
        rank = 1

    if rank < 100000:
        return 1
    else:
        return 0

def iframe(response):
    if response == "":
        return 1
    else:
        if re.findall(r"[<iframe>|<frameBorder>]", response.text):
            return 0
        else:
            return 1

def mouse_over(response): 
    if response == "" :
        return 1
    else:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            return 1
        else:
            return 0

def right_click(response):
    if response == "":
        return 1
    else:
        if re.findall(r"event.button ?== ?2", response.text):
            return 0
        else:
            return 1

def forwarding(response):
    if response == "":
        return 1
    else:
        if len(response.history) <= 2:
            return 0
        else:
            return 1

def get_http_response(url):
    try:
        response = requests.get(url, timeout=5)  # Set a timeout of 5 seconds
        return response
    except requests.exceptions.RequestException as e:
        return None

def extract_features(url):
    features = []
    
    # Address bar based features
    features.append(having_ip(url))
    features.append(have_at_sign(url))
    features.append(get_length(url))
    features.append(get_depth(url))
    features.append(redirection(url))
    features.append(http_domain(url))
    features.append(tiny_url(url))
    features.append(prefix_suffix(url))
    print(url)
    print(have_at_sign(url))
    print(get_length(url))
    print(get_length(url))
    print(get_depth(url))
    print(redirection(url))
    print(http_domain(url))
    print(prefix_suffix(url))

    # Domain based features
    dns = 0
    try:
        domain_name = whois.whois(urlparse(url).netloc)
    except:
        dns = 1
    features.append(dns)
    dns_age = 1 if dns == 1 else domainAge(domain_name)
    dns_end = 1 if dns == 1 else domainEnd(domain_name)
    features.append(web_traffic(url))
    features.append(dns_age)
    features.append(dns_end)
    response = get_http_response(url)

    # HTML & Javascript based features
    try:
        response = requests.get(url)
    except:
        response = ""
    if response is not "":
        features.append(iframe(response))
        features.append(mouse_over(response))
        features.append(right_click(response))
        features.append(forwarding(response))
    else:
        # If response is None, set these features to 0 or None
        features.extend([1, 1, 1, 1])

    return features

def predict_phishing(features):
    # Load the model
    with open('server side\XGBoostClassifier.pickle.dat', 'rb') as file:
        loaded_model = pickle.load(file)

    # Make predictions
    new_data = np.array([features])
    prediction = loaded_model.predict(new_data)
    print(prediction)
    return prediction

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
                features = extract_features(url)
                # Make prediction
                prediction = predict_phishing(features)
                perd = ''
                if prediction[0] == 1:
                    perd = "The AI classified This URL as phishing."
                else:
                    perd = "The AI classified This URL as to be safe."
                mes = f'{findCloseWords(url)}? \n\n {perd} \n '
                print(mes)
                client.sendall(mes.encode())
                client.close()
                return
            print(f"answer: {response}")
            if response == 'Good':
                client.sendall(f'{response}'.encode())
            else:
                features = extract_features(url)
                # Make prediction
                prediction = predict_phishing(features)
                perd = ''
                if prediction[0] == 1:
                    perd = "The AI classified This URL as phishing."
                else:
                    perd = "The AI classified This URL as to be safe."
                mes = f'{response}{findCloseWords(url)}? \n {perd} \n Full dignosis: {features}'
                print(mes)
                client.sendall(mes.encode())
            print("sent answer")
            #client.sendall('404 not found'.encode())
            client.close()
            return
        except:
            time.sleep(0.2)

t = threading.Thread(target=menangeServer)
t.start()
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


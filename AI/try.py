import pickle
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
import xgboost as xgb
from urllib.parse import urlparse
import pandas as pd
import socket  # For DNS record check (if enabled)
import re  # For regular expression-based features
import ipaddress
import re
from bs4 import BeautifulSoup
import whois
import urllib
import urllib.request
from datetime import datetime
import requests
# 1.Domain of the URL (Domain) 
def getDomain(url):  
    domain = urlparse(url).netloc
    if re.match(r"^www.",domain):
        domain = domain.replace("www.","")
    print(domain)
    return domain
# 18.Checks the number of forwardings (Web_Forwards)    
def forwarding(response):
  if response == "":
    print(1)
    return 1
  else:
    if len(response.history) <= 2:
      return 0
    else:
      print(1)
      return 1
# 17.Checks the status of the right click attribute (Right_Click)
def rightClick(response):
  if response == "":
    print(1)
    return 1
  else:
    if re.findall(r"event.button ?== ?2", response.text):
      return 0
    else:
      print(1)
      return 1
# 16.Checks the effect of mouse over on status bar (Mouse_Over)
def mouseOver(response): 
  if response == "" :
    print(1)
    return 1
  else:
    if re.findall("<script>.+onmouseover.+</script>", response.text):
      print(1)
      return 1
    else:
      return 0
# 15. IFrame Redirection (iFrame)
def iframe(response):
  try:
    if response == "":
        print(1)
        return 1
    else:
        if re.findall(r"[<iframe>|<frameBorder>]", response.text):
            return 0
        else:
            return 1
  except:
      return 1
# 14.End time of domain: The difference between termination time and current time (Domain_End) 
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
# 12.Web traffic (Web_Traffic)
def web_traffic(url):
    try:
        #Filling the whitespaces in the URL if any
        url = urllib.parse.quote(url)
        rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find(
            "REACH")['RANK']
        rank = int(rank)
    except:
        print(1)
        return 1
    if rank <100000:
        print(1)
        return 1
    else:
        return 0
# have ip
def havingIP(url):
  try:
    ipaddress.ip_address(url)
    ip = 1
    print(1)
  except:
    ip = 0
  return ip
# 3.Checks the presence of @ in URL (Have_At)
def haveAtSign(url):
  if "@" in url:
    at = 1    
  else:
    at = 0    
  print(at)
  return at
# 4.Finding the length of URL and categorizing (URL_Length)
def getLength(url):
  if len(url) < 54:
    length = 0            
  else:
    length = 1            
  print(length)
  return length
# 5.Gives number of '/' in URL (URL_Depth)
def getDepth(url):
  s = urlparse(url).path.split('/')
  depth = 0
  for j in range(len(s)):
    if len(s[j]) != 0:
      depth = depth+1
  return depth
# 6.Checking for redirection '//' in the url (Redirection)
def redirection(url):
  pos = url.rfind('//')
  if pos > 6:
    if pos > 7:
      print(1)
      return 1
    else:
      return 0
  else:
    return 0
# 7.Existence of “HTTPS” Token in the Domain Part of the URL (https_Domain)
def httpDomain(url):
  domain = urlparse(url).netloc
  if 'https' in domain:
    return 1
  else:
    return 0
#listing shortening services
shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"
# 8. Checking for Shortening Services in URL (Tiny_URL)
def tinyURL(url):
    match=re.search(shortening_services,url)
    if match:
        print(1)
        return 1
    else:
        return 0
# 9.Checking for Prefix or Suffix Separated by (-) in the Domain (Prefix/Suffix)
def prefixSuffix(url):
    if '-' in urlparse(url).netloc:
        print(1)
        return 1            # phishing
    else:
        return 0            # legitimate
# model = xgb.Booster()
# model.load_model(pickle.load(open(r"AI\XGBoostClassifier.pickle.dat", "rb")))
model_path = "AI\XGBoostClassifier.pickle.dat"  # Replace with the actual path
with open(model_path, "rb") as f:
    model = pickle.load(f)

#Function to extract features
def featureExtraction(url,label):
  print(model.get_booster().feature_names)
  features = []
  #Address bar based features (10)
  print('\n getDomain')
#   features.append(getDomain(url))
#   print('\n havingIP')
  features.append(havingIP(url))
  print('\n haveAtSign')
  features.append(haveAtSign(url))
  print('\n getLength')
  features.append(getLength(url))
  print('\n getDepth')
  features.append(getDepth(url))
  print('\n redirection')
  features.append(redirection(url))
  print('\n httpDomain')
  features.append(httpDomain(url))
  print('\n tinyURL')
  features.append(tinyURL(url))
  print('\n prefixSuffix')
  features.append(prefixSuffix(url))
  
  #Domain based features (4)
  dns = 0
  try:
    domain_name = whois.whois(urlparse(url).netloc)
  except:
    dns = 1

  features.append(dns)
  print('\n web_traffic')
  features.append(web_traffic(url))
  features.append(1 if dns == 1 else domainAge(domain_name))
  features.append(1 if dns == 1 else domainEnd(domain_name))
  
  # HTML & Javascript based features (4)
  try:
    response = requests.get(url)
  except:
    response = ""
  print('\n web_traffic')  
  features.append(iframe(response))
  print('\n mouseOver')
  features.append(mouseOver(response))
  print('\n rightClick')
  features.append(rightClick(response))
  print('\n forwarding')
  features.append(forwarding(response))
#   print('\n label')
#   features.append(label)
  
  return features
def predict_phishing(url):
    #converting the list to dataframe
    feature_names = ['Have_IP', 'Have_At', 'URL_Length', 'URL_Depth','Redirection', 
                        'https_Domain', 'TinyURL', 'Prefix/Suffix', 'DNS_Record', 'Web_Traffic', 
                        'Domain_Age', 'Domain_End', 'iFrame', 'Mouse_Over','Right_Click', 'Web_Forwards']

    legi_features = [featureExtraction(url,0)]
    print(f"features: {feature_names}")
    legitimate = pd.DataFrame(legi_features, columns= feature_names)
    print(f"to datafram")
    legitimate.head()
    # input_data = prepare_input_data()
    # print (input_data)
    print('perdiction')
    prediction = model.predict_proba(legitimate)[0][1]  # Get probability of phishing class

    return prediction
#prepare_input_data()
precent = predict_phishing('recovery-support.u718573rwk.ha004.t.justns.ru') * 100
print(f'the website is {precent}% not phishing')
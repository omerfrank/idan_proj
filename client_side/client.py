from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
import socket
import rsa
import pickle
import tkinter
import re
from bleach import clean
def sanitize_html(user_input):
    tags = ['p', 'strong', 'em', 'a']  # Allowed HTML tags (customize as needed)
    attrs = {'a': ['href']}  # Allowed attributes for 'a' tag
    return clean(user_input, tags=tags, attributes=attrs, strip=True)
# Define the directory containing static files (HTML, CSS, etc.)
STATIC_DIR = 'static'

class History:
    def __init__(self) -> None:
        self.journal = []
    def ShowHis(self):
        #create html contet of the history of the client
        html_content =  html_content = """<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Browsing History</title>
        <style>
            body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            text-align: center;
            }

            ul {
            list-style-type: disc;
            margin: 0;
            padding: 0;
            }

            li {
            margin-bottom: 10px;
            }
        </style>
        </head>
        <body>
        <h1>Your Browsing History</h1>
        <ul>
        """

        for item in self.journal:
            html_content += f"    <li>{item}</li>\n"

        html_content += """
        </ul>
        </body>
        </html>
        """
        return html_content
    def AddUrl(self,url):
        self.journal.append(url)        
class ServerHandler:
    def __init__(self,serverIP):
        self.serverIP = serverIP
        print("init ----")
    def checkServer(self):
        # check if the server is alive
        client = socket.socket()
        try:
            client.connect((f'{self.serverIP}', 1729))
        except:
            client.close()
            return '404 server not found'
        client.sendall('new'.encode())
        client.close()
        return 'ok'
    def checkSite(self,site):
        #check with server for if a given url is phishing or not
        print("start the cheking proses \n")
        client = socket.socket()
        try:
            client.connect((f'{self.serverIP}', 1729))
            print("connected to server \n")
        except:
            return '404 server not found'
        client.sendall('check'.encode())
        print("ping server \n ")
        try:
            publicKey = pickle.loads(client.recv(2048))
        except pickle.PicklingError as e:
            return '109 comuunication error'
        print(f'gaoned publicKey:  \n')
        encodedMes = rsa.encrypt(message= bytes(site,'utf-8'),pub_key=publicKey)
        print("encoded the messege seccufuly \n")
        client.sendall(encodedMes)
        print("sended new messege \n ")
        print(type(encodedMes) )
        response = client.recv(2048).decode()
        if response == 'Good':
            try:
                webbrowser.open(f'http://{site}')
                return 1
            except:
                return '404 site found'
        else:
            return response
def alertMessage(site):
    html_text = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dangerous Website Warning</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            height: 100vh;
            background: url('fishalert.jpg') no-repeat center center fixed;
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            color: white;
            font-family: Arial, sans-serif;
        }
        .warning-container {
            background: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
            max-width: 600px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
            animation: flash 1s infinite alternate;
        }
        .warning-container h1 {
            font-size: 2em;
            margin: 0;
            color: #ff4f4f;
        }
        .warning-container p {
            margin: 10px 0;
            font-size: 1.2em;
        }
        .warning-container a {
            color: #ff4f4f;
            text-decoration: underline;
        }
        @keyframes flash {
            0% { opacity: 1; }
            100% { opacity: 0.5; }
        }
        .warning-icon {
            font-size: 4em;
            margin-bottom: 10px;
            color: #ff4f4f;
        }
    </style>
</head>
<body>
    <div class="warning-container">
        <div class="warning-icon">⚠️</div>
        <h1>Dangerous Website</h1>
        <p>The web page <strong>'''+site+'''</strong> is not safe and contains malware. DO NOT ENTER.</p>
        <p>For more information on staying safe online, visit 
            <a href="https://www.staysafeonline.org/">StaySafeOnline.org</a>.
        And continue to use fishguerd
        </p>
    </div>
</body>
</html>
'''
    return html_text        
class MyHandler(BaseHTTPRequestHandler):
    """
    Custom handler for handling HTTP requests.
    """
    
    def do_GET(self):
        """
        Handles GET requests (serving static files).
        """
        requested_url = sanitize_html(self.path)
        print(f"\n requested_url: {requested_url} \n")
        #if requested_url == '/':

        # Construct the absolute path to the requested file
        full_path = "client_side"
        try:
            if '.' in self.path:
                filetype = self.path.split('.')[1]
                filename = self.path.split('.')[0]
            else:
                filetype = 'html'
                filename = 'iindex'
            if filetype in ["jpg", "gif"]:
                content_type = "image/jpeg"
            elif filetype == "html":
                content_type = 'text/html; charset=UTF-8'
            elif filetype == 'css':
                content_type ="Content-Type: text/css"
            elif filetype in ['mp4','WebM','OGG']:
                content_type =f"Content-Type: video/{filetype}"
            elif filetype == 'ico':
                content_type = "Content-Type: image/x-icon;"
            else:
                self.send_error(415, 'unsupported media type ')
                return
        except Exception as e:
            # Handle other potential errors
            print(f"Error serving file: {e}")
            self.send_error(500, 'Internal Server Error')            
        try:
            self.send_response(200)  # OK status code
            self.send_header('Content-Type', content_type)
            self.end_headers()
            # handle html requst
            filename = filename[1:] + "." + filetype
            print (f'try to open file {filename}')
            with open(full_path + f"\{filename}", 'rb') as f:
                file_data = f.read()
                self.wfile.write(file_data)
        except FileNotFoundError:
            # Handle file not found case (404 Not Found)
            self.send_error(404, 'File not found')
        except Exception as e:
            # Handle other potential errors
            print('here')
            print(f"Error serving file: {e}")
            self.send_error(500, 'Internal Server Error')

    def do_POST(self):
        """
        Handles POST requests (form submission).
        """
        response = self.path
        if response == '/submit':
            # Read the form data from POST request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()

            # Extract the submitted text from form data
            form_data = dict(item.split('=') for item in post_data.split('&'))
            submitted_text = form_data.get('text')
            submitted_text = sanitize_html(submitted_text)
            try:
                self.server.history.AddUrl(submitted_text)
            except:
                self.server.history = History()
                self.server.history.AddUrl(submitted_text)
            # Process the submitted text (e.g., print it)
            print(f"Received text: {submitted_text}")

            # Send a simple response (you can customize this)
            #try:
            response = self.server.ServerHandel.checkSite(submitted_text)
            self.send_response(200)
            if response == 1:
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"the web page {submitted_text} is safe".encode())
            elif  'Mal' in response:
                self.send_header('Content-Type', 'text/html,charset=UTF-8')
                self.end_headers()
                self.wfile.write(alertMessage(submitted_text).encode())
                return
                #self.wfile.write(f"the web page {submitted_text} is not safe, and contain malwer. DO NOT ENTER".encode())

            elif response == '404 server not found':
                self.send_error(404, 'Server Not Found.\n try insert ip agin')
            elif response == '404 not found':
                self.send_error(404, 'Web page Not Found.\n try insert name agin')
            elif response == '109 comuunication error':
                self.send_error(109, 'communication with server error. \n please try agein')
            else:
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"the web page {submitted_text} is unkwon. \n enter at your own risk \n  {response}".encode())

                    
            #except:
                
        elif response == '/serverIP':
            # Read the form data from POST request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()

            # Extract the submitted text from form data
            form_data = dict(item.split('=') for item in post_data.split('&'))
            submitted_text = form_data.get('text')
            submitted_text = sanitize_html(submitted_text)

            # Process the submitted text (e.g., print it)
            print(f"Received text: {submitted_text}")
            try:
                if re.fullmatch(pattern='^(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])$',string=submitted_text) == None:
                    self.send_error(422,'not a legal ip')
                    return
                #self.ServerHandel = ServerHandler(submitted_text)
                self.server.ServerHandel = ServerHandler(submitted_text)
                print ("xxxxxx \n " + self.server.ServerHandel.serverIP)
                # Send a simple response (you can customize this)
                if self.server.ServerHandel.checkServer() == 'ok':
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(f"successfully entered ip adress! You entered: {submitted_text}".encode())
                else:
                    self.send_error(404, 'Server Not Found')
            except:
                self.send_error(404, 'Server Not Found')
        elif response == '/history':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=UTF-8')
            self.end_headers()
            self.wfile.write(self.server.history.ShowHis().encode())
            
        else:
            # Handle invalid POST requests (404 Not Found)
            self.send_error(404, 'Not Found')

def main():
    """
    Starts the HTTP server.
    """
    port = 8000  # Change port if needed
    httpd = HTTPServer(('', port), MyHandler)
    print(f"Serving at port {port}")
    webbrowser.open('http://localhost:8000/')
    httpd.serve_forever()

if __name__ == '__main__':
    main()
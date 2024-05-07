from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import webbrowser
import socket
import rsa
import pickle


# Define the directory containing static files (HTML, CSS, etc.)
STATIC_DIR = 'static'
class ServerHandler:
    def __init__(self,serverIP):
        self.serverIP = serverIP
        print("init ----")
    def checkServer(self):
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
        elif response == 'Mal':
            return -1
        else:
            return 'unknown'
        
        
class MyHandler(BaseHTTPRequestHandler):
    """
    Custom handler for handling HTTP requests.
    """
    def do_GET(self):
        """
        Handles GET requests (serving static files).
        """
        requested_url = self.path
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
        if self.path == '/submit':
            # Read the form data from POST request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()

            # Extract the submitted text from form data
            form_data = dict(item.split('=') for item in post_data.split('&'))
            submitted_text = form_data.get('text')

            # Process the submitted text (e.g., print it)
            print(f"Received text: {submitted_text}")

            # Send a simple response (you can customize this)
            #try:
            response = self.server.ServerHandel.checkSite(submitted_text)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            if response == 1:
                self.wfile.write(f"the web page {submitted_text} is safe".encode())
            elif response == -1:
                self.wfile.write(f"the web page {submitted_text} is not safe, and contain malwer. \n enter at your own risk".encode())
            elif response == '404 server not found':
                self.send_error(404, 'Server Not Found.\n try insert ip agin')
            elif response == '404 not found':
                self.send_error(404, 'Web page Not Found.\n try insert name agin')
            elif response == 'unknown':
                self.wfile.write(f"the web page {submitted_text} is unkwon. \n enter at your own risk".encode())
            elif response == '109 comuunication error':
                self.send_error(109, 'communication with server error. \n please try agein')
                    
            #except:
                
        elif self.path == '/serverIP':
            # Read the form data from POST request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()

            # Extract the submitted text from form data
            form_data = dict(item.split('=') for item in post_data.split('&'))
            submitted_text = form_data.get('text')

            # Process the submitted text (e.g., print it)
            print(f"Received text: {submitted_text}")
            try:
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

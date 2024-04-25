from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# Define the directory containing static files (HTML, CSS, etc.)
STATIC_DIR = 'static'

class MyHandler(BaseHTTPRequestHandler):
    """
    Custom handler for handling HTTP requests.
    """
    def do_GET(self):
        """
        Handles GET requests (serving static files).
        """
        requested_url = self.path
        #if requested_url == '/':
        requested_url = '/index.html'  # Serve index.html for root path

        # Construct the absolute path to the requested file
        full_path = "client_side\index.html"
        print(full_path)

        try:
            with open(full_path, 'rb') as f:
                file_data = f.read()
                content_type = 'text/html; charset=UTF-8'  # Set appropriate content type
                self.send_response(200)  # OK status code
                self.send_header('Content-Type', content_type)
                self.end_headers()
                self.wfile.write(file_data)
        except FileNotFoundError:
            # Handle file not found case (404 Not Found)
            self.send_error(404, 'File not found')
        except Exception as e:
            # Handle other potential errors
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
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Form submitted successfully! You entered: {submitted_text}".encode())
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
    httpd.serve_forever()

if __name__ == '__main__':
    main()

import socket
import base64

def read_image_content(image_path):
    with open(image_path, "rb") as image_file:
        image_content = image_file.read()
        print(base64.b64encode(image_content).decode('utf-8'))
        return base64.b64encode(image_content).decode('utf-8')
def generate_html_response(content,img_content,vid_content):
    html_content = f"""
    <html>
    <head>
        <title>site</title>
        <link rel="icon" type="image/x-icon" href="data:image/JPG;Base64,{read_image_content(img_content)}">
        <style>
            /* Center the text and apply some styles */
            .centered-text {{
                text-align: center;
                font-size: 24px;
                color: blue;
                /* Add any other styles you want */
            }}
        </style>
    </head>
    <body>
        <div class="centered-text">{content}
        <h2>HTML Image</h2>
        <img src="data:image/JPG;Base64,{read_image_content(img_content)}" alt="Trulli" width="500" height="333">
        </div>
        <video width="320" height="240" autoplay muted controls loop>
        <source src="data:video/mp4;base64,{read_image_content(vid_content)}" type="video/mp4">
        alt = "no"
        </video>

    </body>
    </html>
    """
    return html_content

website = socket.socket()
website.bind(('localhost', 1729))  # Change 'localhost' to your server's IP address
website.listen()

while True:
    user, address = website.accept()
    request = user.recv(1024).decode()
    print(request)

    content = generate_html_response("ziv",img_content=r"C:\Users\omerf\OneDrive\שולחן העבודה\idan_proj\client side\FishGuardLogo2.jpg",vid_content= r"C:\Users\omerf\OneDrive\שולחן העבודה\tomer\idan&UDI\imeges\yair.mp4")  # Your centered word here
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{content}"
    user.send(response.encode())
    user.close()
 
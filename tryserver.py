import customtkinter as ctk
from tkinter import messagebox, END, Listbox, Tk, font as TkFont
from PIL import Image, ImageTk
import threading
import socket
import select

class BackEnd:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((socket.gethostbyname(socket.gethostname()), 1729))
        self.ip = socket.gethostbyname(socket.gethostname())
        print(f"Server listening on {self.ip}:1729")

    def runServer(self):
        """Run the server in a separate thread."""
        self.server.listen()
        self.clients = []
        while True:
            rlist, _, _ = select.select([self.server] + self.clients, [], [])
            for ready in rlist:
                if ready is self.server:
                    client, _ = self.server.accept()
                    self.clients.append(client)
                    print("Client connected")
                    t = threading.Thread(target=self.handleClients, args=(client,))
                    t.start()
                else:
                    try:
                        data = ready.recv(1024)
                        if data:
                            print(f"Received data: {data}")
                            # Handle received data here
                        else:
                            ready.close()
                            self.clients.remove(ready)
                    except ConnectionResetError:
                        print("Client disconnected")
                        self.clients.remove(ready)

    def handleClients(self, client_socket):
        """Handle client communication in a separate thread."""
        while True:
            try:
                message = client_socket.recv(1024)
                if message:
                    print(f"Client says: {message.decode()}")
                else:
                    break
            except ConnectionResetError:
                print("Client forcibly closed the connection")
                break
        client_socket.close()

def start_server():
    """Starts the server in a separate thread and copies the IP to clipboard."""
    server = BackEnd()
    t = threading.Thread(target=server.runServer)
    t.daemon = True  # Allow thread to exit when main program exits
    t.start()
    # Copy the server IP to the clipboard
    root.clipboard_clear()
    root.clipboard_append(server.ip)
    root.update()  # Keep the clipboard content after the window is closed
    messagebox.showinfo("Server", f"Server started successfully!\nServer IP copied to clipboard: {server.ip}")

def open_updates():
    """Opens the updates window with client request list and filtering options."""
    updates_window = ctk.CTkToplevel(main_window)
    updates_window.title("Updates")
    updates_window.geometry("500x400")
    
    # Add 'Client Requests' list box
    client_request_label = ctk.CTkLabel(updates_window, text="Client Requests", pady=10)
    client_request_label.pack(pady=5)
    
    client_request_listbox = Listbox(updates_window, height=10, width=50, font=TkFont.Font(size=12))
    client_request_listbox.pack(pady=5)
    
    # Populate listbox with sample data (for demonstration)
    sample_data = [
        "Request 1: Potential phishing attempt",
        "Request 2: Safe",
        "Request 3: Phishing attempt detected",
        "Request 4: Safe",
        "Request 5: Safe",
        "Request 6: Phishing attempt detected"
    ]
    for item in sample_data:
        client_request_listbox.insert(END, item)
    
    # Add 'Show Only Phishing Attempts' checkbox
    show_phishing_var = ctk.StringVar(value="off")
    show_phishing_checkbox = ctk.CTkCheckBox(
        updates_window,
        text="Show Only Phishing Attempts",
        variable=show_phishing_var,
        onvalue="on",
        offvalue="off",
        command=lambda: filter_requests(show_phishing_var.get(), client_request_listbox, sample_data)
    )
    show_phishing_checkbox.pack(pady=10)
    
    # Add 'Back' button to return to main window
    back_button = ctk.CTkButton(updates_window, text="Back", command=updates_window.destroy, corner_radius=10, fg_color='#E53935', text_color='white')
    back_button.pack(pady=10)

def filter_requests(show_phishing, listbox, data):
    """Filters the listbox items based on phishing attempts."""
    listbox.delete(0, END)
    if show_phishing == "on":
        filtered_data = [item for item in data if "Phishing attempt detected" in item]
    else:
        filtered_data = data
    for item in filtered_data:
        listbox.insert(END, item)

def main():
    """Main function to initialize and run the GUI application."""
    global main_window, root  # Declare main_window and root as global to be accessible in other functions
    
    # Create the main window
    root = Tk()  # Create a root Tk instance for clipboard operations
    main_window = ctk.CTk()
    main_window.title("Fishgurd Application")
    main_window.geometry("500x500")
    main_window.configure(fg_color='lightblue')  # Set background color
    
    # Resize the logo image
    original_image = Image.open(r"C:\Users\omerf\OneDrive\שולחן העבודה\idan_proj\FishLogo2.png")
    image_width, image_height = original_image.size
    # Resize image to fit within 400x300 while maintaining aspect ratio
    max_width, max_height = 400, 300
    if image_width > max_width or image_height > max_height:
        ratio = min(max_width / image_width, max_height / image_height)
        new_size = (int(image_width * ratio), int(image_height * ratio))
        resized_image = original_image.resize(new_size, Image.Resampling.LANCZOS)
    else:
        resized_image = original_image
    
    logo = ImageTk.PhotoImage(resized_image)
    
    # Add a logo
    logo_label = ctk.CTkLabel(main_window, image=logo, padx=10, pady=10)
    logo_label.pack(pady=20)
    
    # Add "Start Server" button
    start_server_button = ctk.CTkButton(main_window, text="Start Server", command=start_server, corner_radius=10, fg_color='#4CAF50', text_color='white')
    start_server_button.pack(pady=10)
    
    # Add "Updates" button
    updates_button = ctk.CTkButton(main_window, text="Updates", command=open_updates, corner_radius=10, fg_color='#2196F3', text_color='white')
    updates_button.pack(pady=10)
    
    # Run the application
    main_window.mainloop()

if __name__ == "__main__":
    main()

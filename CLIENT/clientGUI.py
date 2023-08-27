import tkinter as tk
from tkinter import filedialog, messagebox
import client


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Client")
        
        # Create frames
        self.login_frame = tk.Frame(root)
        self.main_frame = tk.Frame(root)

        # Initialize login widgets
        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_entry = tk.Entry(self.login_frame)
        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_entry = tk.Entry(self.login_frame, show="*")

        self.server_ip_label = tk.Label(self.login_frame, text="Server IP:")
        self.server_ip_entry = tk.Entry(self.login_frame)

        self.thisclient_ip_label = tk.Label(self.login_frame, text="Local IP:", )
        self.thisclient_ip_entry = tk.Entry(self.login_frame)
        

        self.thisclient_ip_entry.insert(0, "{}".format(client.getClientIP()))
        self.thisclient_ip_entry.configure(fg="#0078d4",selectbackground='#00ffff',selectforeground='#0000ff')
        self.thisclient_ip_entry.config(state="readonly")





        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)

        # Pack login widgets
        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.server_ip_label.pack()
        self.server_ip_entry.pack()
        self.thisclient_ip_label.pack()
        self.thisclient_ip_entry.pack()

        self.login_button.pack()

        # Initialize main application widgets
        self.browse_button = tk.Button(self.main_frame, text="Browse Files and Upload", command=self.browse_files)
        self.download_button = tk.Button(self.main_frame, text="Download", command=self.download_file)
        self.delete_button = tk.Button(self.main_frame, text="Delete", command=self.delete_file)

        self.fileName_label = tk.Label(self.main_frame, text="  FILES   ")
        self.fileName_entry = tk.Listbox(self.main_frame, width=40,)
 
        # Pack main application widgets
        self.browse_button.pack()
        self.download_button.pack()
        self.delete_button.pack()
        self.fileName_label.pack()
        self.fileName_entry.pack()

        # Pack the login frame initially
        self.login_frame.pack()
        self.filesArray = []
        
    def update_files_listbox(self):
        self.filesArray = client.GetClientFiles()
        self.fileName_entry.delete(0, tk.END)
        for file in self.filesArray:
            self.fileName_entry.insert(tk.END, f'{file}' )

    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        serverIP = self.server_ip_entry.get()
       
        # Check if the credentials are valid
        if username and password and serverIP:
            response = client.connectWithServerAndLogin(serverIP, username, password)
            if response == "server_error":
                self.show_error_message("Connection error with the wanted server. | Ckeck Server IP")
            elif response == "successfully_login":
                self.login_frame.pack_forget()
                self.main_frame.pack()
                self.update_files_listbox()
            elif response == "Blocked_IP":
                self.show_error_message("Connection refused by the target server. | BLOCKED IP")
            elif response == "Blocked_username":
                self.show_error_message("Connection refused by the target server. | BLOCKED USER")
            elif response == "wrong_username_password":
                self.show_error_message("Invalid Username or Password")  
            elif response == "user_doesnt_exist": 
                self.show_error_message("User Doesn't Exist In the System")
        else:
            # Show an error message for invalid credentials
            self.show_error_message("Invalid Input. Enter the 3 credentials.")

    def show_error_message(self, message):
        # Function to display error messages in a messagebox
        tk.messagebox.showerror("Error", message)

    def browse_files(self):
        # Function to handle the "Browse Files" button click
        file_path = filedialog.askopenfilename()
        if file_path:
            # Do something with the selected file path, e.g., display the file name
            tk.messagebox.showinfo("Selected File", f"Selected file: {file_path}")
            client.uploadFile(file_path)
            self.update_files_listbox()
    
    def download_file(self):
        # Function to handle the "Download" button click
        # Add your download logic here, e.g., download the file from a server
        # For simplicity, we'll just show a message box
        selected_index = self.fileName_entry.curselection()
        if selected_index:
            name = self.filesArray[selected_index[0]]
            client.getFileByName(name)
            tk.messagebox.showinfo("Download", "File download completed.")


    def delete_file(self):
        # Function to handle the "Download" button click
        # Add your download logic here, e.g., download the file from a server
        # For simplicity, we'll just show a message box
        selected_index = self.fileName_entry.curselection()
        if selected_index:
            name = self.filesArray[selected_index[0]]
            response = messagebox.askyesno("Confirmation", f"Are you sure you want to delete {name} from the server?")
            if response == tk.YES:
                client.deleteFileByName(name)
                self.update_files_listbox()
                tk.messagebox.showinfo("Delete", "File Deletion completed.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")  # Set the initial size to 400 pixels wide and 200 pixels tall
    app = App(root)
    root.mainloop()

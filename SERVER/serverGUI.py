import tkinter as tk
from tkinter import simpledialog, messagebox
import tkinter.ttk as ttk
import re
import api
import server


network_users = api.fetchAllUsers()
blocked_ips = api.fetchBlockedIPs()
print(blocked_ips)
def on_add_user():
    username = entry_username.get()
    password = entry_password.get()
    firstName = entry_firstName.get()
    lastName = entry_lastName.get()
    status = selected_status.get()

    if username and password and firstName and lastName and status:
        api.addUser(username, password, firstName, lastName, status)
        user_info = {
            "username": username,
            "password": password,
            "firstName": firstName,
            "lastName": lastName,
            "status": status
        }
        network_users.append(user_info)
        update_listbox()
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        entry_firstName.delete(0, tk.END)
        entry_lastName.delete(0, tk.END)
        selected_status.set("Allowed")
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")



def on_remove_user():
    selected_index = list_users.curselection()
    if selected_index:
        index = selected_index[0]
        user = network_users[index]["username"]
        response = messagebox.askyesno("Confirmation", f"Are you sure you want to remove {user}?")
        if response == tk.YES:
            userFiles = api.fetchAllFiles(user)
            for file in userFiles:
                server.deleteFileFromServer(file)
            api.deleteUser(user)
            del network_users[index]
            update_listbox()



def on_update_user():
    selected_index = list_users.curselection()
    if selected_index:
        index = selected_index[0]
        user = network_users[index]
        new_username = simpledialog.askstring("Update Username", "Enter new username:", initialvalue=user["username"], parent=root)
        new_password = simpledialog.askstring("Update Password", "Enter new password:", show="*", initialvalue=user["password"], parent=root)
        new_firstName = simpledialog.askstring("Update First Name", "Enter new first name:", initialvalue=user["firstName"], parent=root)
        new_lastName = simpledialog.askstring("Update Last Name", "Enter new last name:", initialvalue=user["lastName"], parent=root)
        result = messagebox.askokcancel("Update Status", "Update Status:", icon="question", detail="", parent=root)

        if new_username is not None and new_password is not None and new_firstName is not None and new_lastName is not None:
            if result == True:
                if user["status"] == "Blocked":
                    user["status"] = "Allowed"
                else:
                    user["status"] = "Blocked"

            api.updateUser(user["username"], new_username, new_password, new_firstName, new_lastName, user["status"])
            network_users[index]["username"] = new_username
            network_users[index]["password"] = new_password
            network_users[index]["firstName"] = new_firstName
            network_users[index]["lastName"] = new_lastName
            update_listbox()


def update_listbox():
    list_users.delete(0, tk.END)
    for user in network_users:
        list_users.insert(tk.END, f'{user["username"]} | {user["firstName"] + " " + user["lastName"]} | {user["status"]}' )


def update_ip_listbox():
    blocked_ips_list.delete(0, tk.END)
    for ip in blocked_ips:
        blocked_ips_list.insert(tk.END, f'{ip}' )


def add_ip():
    ip = ip_entry.get()
    if ip and ip not in blocked_ips_list.get(0, tk.END):
        pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        x = pattern.match(ip)
        if not x:
            messagebox.showwarning("Warning", "Please enter a proper IP address.")
            ip_entry.delete(0, tk.END)
        else:
            api.addIP(ip)
            blocked_ips_list.insert(tk.END, ip)
            blocked_ips.append(ip)
            ip_entry.delete(0, tk.END)
    print(blocked_ips)  

def delete_ip():
    selected_index = blocked_ips_list.curselection()
    print(blocked_ips)
    print(selected_index)
    if selected_index:
        index = selected_index[0]
        ip = blocked_ips[index]
        response = messagebox.askyesno("Confirmation", f"Are you sure you want to delete ip: {ip}?")
        if response == tk.YES:
            api.deleteIP(ip)
            del blocked_ips[index]
            update_ip_listbox()  
    print(blocked_ips)     
        

# Main application window
root = tk.Tk()
root.title("Network Users Manager")

# Define colors
bg_color = "#f0f0f0"
button_bg_color = "#0078d4"
button_fg_color = "white"

# Set background color
root.configure(background=bg_color)

# Listbox to display users
list_users = tk.Listbox(root, selectmode=tk.SINGLE, width=40, bg=bg_color)
list_users.grid(row=0, column=0, padx=10, pady=5, rowspan=5)
update_listbox()

# Buttons to interact with the user list
btn_remove_user = tk.Button(root, text="Remove User", command=on_remove_user, bg=button_bg_color, fg=button_fg_color)
btn_remove_user.grid(row=1, column=1, padx=5, pady=5, sticky="w")

btn_update_user = tk.Button(root, text="Update User", command=on_update_user, bg=button_bg_color, fg=button_fg_color)
btn_update_user.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Separator
separator = ttk.Separator(root, orient="vertical")
separator.grid(row=0, column=2, rowspan=6, sticky="ns", padx=5)

# Entry widgets and labels for user information
label_username = tk.Label(root, text="Username:", bg=bg_color)
label_username.grid(row=0, column=3, padx=5, pady=5, sticky="e")
entry_username = tk.Entry(root, width=30)
entry_username.grid(row=0, column=4, padx=5, pady=5)

label_password = tk.Label(root, text="Password:", bg=bg_color)
label_password.grid(row=1, column=3, padx=5, pady=5, sticky="e")
entry_password = tk.Entry(root, width=30, show="*")  # Password field (characters are hidden)
entry_password.grid(row=1, column=4, padx=5, pady=5)

label_firstName = tk.Label(root, text="First Name:", bg=bg_color)
label_firstName.grid(row=2, column=3, padx=5, pady=5, sticky="e")
entry_firstName = tk.Entry(root, width=30)
entry_firstName.grid(row=2, column=4, padx=5, pady=5)

label_lastName = tk.Label(root, text="Last Name:", bg=bg_color)
label_lastName.grid(row=3, column=3, padx=5, pady=5, sticky="e")
entry_lastName = tk.Entry(root, width=30)
entry_lastName.grid(row=3, column=4, padx=5, pady=5)

# Radio buttons for user status
selected_status = tk.StringVar(value="Allowed")
label_status = tk.Label(root, text="Status:", bg=bg_color)
label_status.grid(row=4, column=3, padx=5, pady=5, sticky="e")

radio_allowed = tk.Radiobutton(root, text="Allowed", variable=selected_status, value="Allowed", bg=bg_color)
radio_allowed.grid(row=4, column=4, padx=5, pady=5, sticky="w")

radio_blocked = tk.Radiobutton(root, text="Blocked", variable=selected_status, value="Blocked", bg=bg_color)
radio_blocked.grid(row=4, column=4, padx=5, pady=5, sticky="e")

# Add User button
btn_add_user = tk.Button(root, text="Add User", command=on_add_user, bg=button_bg_color, fg=button_fg_color)
btn_add_user.grid(row=5, column=4, padx=5, pady=5, sticky="e")


# Horizontal Separator
ip_separator = ttk.Separator(root, orient="horizontal")
ip_separator.grid(row=9, column=0, columnspan=5, padx=10, pady=5, sticky="ew")



# Create and place components
server_ip_label = tk.Label(root, text="Server IP Address:")
server_ip_label.grid(row=10, column=1, padx=10, pady=5, sticky="e")

server_ip_entry = tk.Entry(root, width=30)
server_ip_entry.grid(row=10, column=2, padx=10, pady=5)
server_ip_entry.insert(0, "{}: {}".format(server.getServerIP() ,server.getServerPortNumber()))
server_ip_entry.configure(fg=button_bg_color,selectbackground='#00ffff',selectforeground='#0000ff')
server_ip_entry.config(state="readonly")



ip_label = tk.Label(root, text="Enter IP Address:")
ip_label.grid(row=11, column=1, padx=10, pady=5, sticky="e")

ip_entry = tk.Entry(root, width=30)
ip_entry.grid(row=11, column=2, padx=10, pady=5)

add_button = tk.Button(root, text="Add Blocked IP", command=add_ip, bg=button_bg_color, fg=button_fg_color)
add_button.grid(row=11, column=3, padx=10, pady=5, sticky="e")



blocked_ips_list = tk.Listbox(root, selectmode=tk.SINGLE, width=30, bg=bg_color)
blocked_ips_list.grid(row=13, column=2, padx=10, pady=5)
update_ip_listbox()

delete_button = tk.Button(root, text="Delete Selected IP", command=delete_ip, bg=button_bg_color, fg=button_fg_color)
delete_button.grid(row=13, column=3, padx=10, pady=5, sticky="e")

root.mainloop()


import socket
import threading
import api
import os
import pickle


# device's IP address
SERVER_HOST = "localhost"
SERVER_PORT = 5005
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"


s = socket.socket()
s.bind(('', SERVER_PORT))
s.listen(5)


def deleteFileFromServer(name):
    os.remove("FILES\\" + name)

def getServerIP():
    return socket.gethostbyname(socket.gethostname())


def getServerPortNumber():
    return SERVER_PORT


def receiveFiles(client_socket, username):
    while True:
        data = client_socket.recv(BUFFER_SIZE).decode()
        if not data:
            continue
        requestType = data.split(SEPARATOR)[0]
        if requestType == "GET_ALL":
            client_socket.send(pickle.dumps(api.fetchAllFiles(username)));
        elif requestType == "GET_FILE":
            fileName = data.split(SEPARATOR)[1]
            file_path = "FILES\\" + fileName
            fileSize = os.path.getsize(file_path)
            client_socket.send(f"{fileName}{SEPARATOR}{fileSize}".encode())
            with open(file_path, "rb") as f:
                while True:
                    # read the bytes from the file
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        # file transmitting is done
                        break
                    client_socket.sendall(bytes_read)
        elif requestType == "DELETE_FILE":
            fileName = data.split(SEPARATOR)[1]
            api.deleteFile(fileName)
            os.remove("FILES\\" + fileName)
        elif requestType == "UPLOAD_TO_SERVER":
            fileName = data.split(SEPARATOR)[1]
            fileSize = data.split(SEPARATOR)[2]
            fileSize = int(fileSize)
            received_data = b""  
            unique_filename = api.addFile(username, fileName)
            with open("FILES\\" + unique_filename, "wb") as f:
                while fileSize > 0:
                    data = client_socket.recv(min(BUFFER_SIZE, fileSize))
                    fileSize -= len(data) 
                    received_data += data  
                    if not data:
                        break
                f.write(received_data) 
        


def main():
    while True:
        print(f"[*] Listening as {getServerIP()}:{SERVER_PORT}")
        global s
        # accept connection if there is any
        client_socket, address = s.accept()
        # if below code is executed, that means the sender is connected
        print(f"[+] {address} is connected.")
        received = client_socket.recv(BUFFER_SIZE).decode()
        username, password = received.split(SEPARATOR)
        response = api.login(address[0], username, password)
        client_socket.send(response.encode());
        if response == "successfully_login":
            print(username , " connected")
            clientThread = threading.Thread(target=receiveFiles,args=(client_socket, username))
            clientThread.start()
        # receive the file infos
        # receive using client socket, not server socket


x = threading.Thread(target=main, daemon=True)
x.start()
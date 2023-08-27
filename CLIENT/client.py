import socket
import os
import pickle
import sys




SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step
# the ip address or hostname of the server, the receiver
host = "localhost"

port = 5005




print(sys.argv)

def getClientIP():

    return socket.gethostbyname(socket.gethostname())

def connectWithServerAndLogin(serverIP, username, password):
# create the client socket

    global s    
    print(f"[+] Connecting to {serverIP}:{port}")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((serverIP, port))
        print("[+] Connected.")
    except socket.error as e:
        return "server_error"
    # send the filename and filesize
    s.send(f"{username}{SEPARATOR}{password}".encode())
    response = s.recv(BUFFER_SIZE);
    return response.decode();
    

def uploadFile(file_path):
    global s
    fileName = os.path.basename(file_path).split('/')[-1]
    fileSize = os.path.getsize(file_path)
    s.send(f"UPLOAD_TO_SERVER{SEPARATOR}{fileName}{SEPARATOR}{fileSize}".encode())
    print(fileName, fileSize)
    with open(file_path, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in 
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar

def GetClientFiles():
    global s
    s.send(f"GET_ALL".encode())
    response = s.recv(BUFFER_SIZE);
    return pickle.loads(response);


def getFileByName(name):
    global s
    s.send(f"GET_FILE{SEPARATOR}{name}".encode())
    received = s.recv(BUFFER_SIZE).decode()
    fileName, fileSize = received.split(SEPARATOR)
    fileSize = int(fileSize)
    received_data = b"" 
    with open(fileName, "wb") as f:
        while fileSize > 0:
            data = s.recv(min(BUFFER_SIZE, fileSize))
            fileSize -= len(data) 
            received_data += data  
            if not data:
                break
        f.write(received_data)


def deleteFileByName(name):
    global s
    s.send(f"DELETE_FILE{SEPARATOR}{name}".encode())
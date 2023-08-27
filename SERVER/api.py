from dbConnection import connect

mydb = connect()
mycursor = mydb.cursor()


def fetchAllUsers():
    network_users = []
    mycursor.execute("SELECT * FROM users")
    users = mycursor.fetchall()
    for user in users:
        if user[5] == 1:
            x = {
            "username": user[1],
            "password": user[2],
            "firstName": user[3],
            "lastName": user[4],
            "status": "Blocked"
            }
            network_users.append(x)
        else:
            x = {
            "username": '{}'.format(user[1]),
            "password": user[2],
            "firstName": user[3],
            "lastName": user[4],
            "status": "Allowed"
            }
            network_users.append(x)
            
    return network_users


def addUser(username, password, firstName, lastName, status):
    sql = "INSERT INTO users (userName, password, firstName, lastName, status) VALUES (%s, %s, %s, %s, %s)"
    if status == "Allowed":
        val = (username, password, firstName, lastName, False)
    else:
        val = (username, password, firstName, lastName, True)
    mycursor.execute(sql, val)
    mydb.commit()



def deleteUser(username):
    sql = "DELETE FROM users WHERE userName = %s"
    name = (username)
    mycursor.execute(sql, name)
    mydb.commit()
    


def updateUser(old_username, new_username, new_password, new_firstName, new_lastName, new_status):
    if new_status == "Blocked":
            new_status = True
    else:
        new_status = False
    sql = "UPDATE users SET userName = %s, password = %s, firstName = %s, lastName = %s, status = %s WHERE userName = %s"
    val = (new_username, new_password, new_firstName, new_lastName, new_status, old_username)
    mycursor.execute(sql, val)
    mydb.commit()

def fetchUserID(username):
    sql = "SELECT * FROM users WHERE userName = %s"
    adr = (username)
    mycursor.execute(sql, adr)
    user = mycursor.fetchall()
    return user[0][0]
# ----------------------------------------------------------------------------------------------------------

def fetchBlockedIPs():
    blocked_ips = []
    mycursor.execute("SELECT * FROM ip_blocked")
    ips = mycursor.fetchall()
    for ip in ips:
        blocked_ips.append(ip[1])
    return blocked_ips



def addIP(ip_address):
    sql = "INSERT INTO ip_blocked (ip_address) VALUES (%s)"
    val = (ip_address)
    mycursor.execute(sql, val)
    mydb.commit()


def deleteIP(ip_address):
    sql = "DELETE FROM ip_blocked WHERE ip_address = %s"
    adr = (ip_address)
    mycursor.execute(sql, adr)
    mydb.commit()

# ------------------------------------------------------------------------------------------

def login(ipAddress, username, password):
    sql = "SELECT * FROM ip_blocked WHERE ip_address = %s"
    adr = (ipAddress)
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()
    if myresult:
        return "Blocked_IP"
    else:
        sql = "SELECT * FROM users WHERE userName = %s"
        adr = (username)
        mycursor.execute(sql, adr)
        myresult = mycursor.fetchall()
        if myresult:
            if myresult[0][5] == 1:
                return "Blocked_username"
            else:
                if myresult[0][2] == password:
                    return "successfully_login"
                else:
                    return "wrong_username_password"
        else:
            return "user_doesnt_exist"

# ----------------------------------------------------------------------------------


def addFile(username, fileName):
    user_ID = fetchUserID(username)
    sql = "INSERT INTO files (user_ID) VALUES (%s)"
    val = (user_ID)
    mycursor.execute(sql, val)
    mydb.commit()
    rowID = mycursor.lastrowid
    unique_filename = str(rowID) + "_" + fileName
    sql = "UPDATE files SET fileName = %s WHERE id = %s"
    val = (unique_filename, rowID)
    mycursor.execute(sql, val)
    mydb.commit()
    return unique_filename


def fetchAllFiles(username):
    filesList = []
    user_ID = fetchUserID(username)
    sql = "SELECT fileName FROM files WHERE user_ID = %s"
    adr = (user_ID)
    mycursor.execute(sql, adr)
    files = mycursor.fetchall()
    for file in files:
        filesList.append(file[0])
    return filesList

def deleteFile(name):
    sql = "DELETE FROM files WHERE fileName = %s"
    adr = (name)
    mycursor.execute(sql, adr)
    mydb.commit()
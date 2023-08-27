import pymysql

def connect():
    connection = pymysql.connect(host="localhost", port=3306, user="root", passwd="", database="network_management_db")
    return connection;





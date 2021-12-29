import pymysql

def obtain_connection():
    return pymysql.connect(host="localhost", user="root", password="perrococo1", db="notesD")

from bd import obtain_connection
import hashlib

def create_user(email, name, password):
    hashPassword = hashlib.md5(password.encode('utf-8')).hexdigest()
    con = obtain_connection()
    with con.cursor() as cursor:
        cursor.execute("INSERT INTO users (email, name, password) VALUES (%s, %s, %s)", (email, name, hashPassword))
    con.commit()
    con.close()

def get_userByEmail(email):
    con = obtain_connection()
    user = []
    with con.cursor() as cursor:
        cursor.execute("SELECT id, email, name, password FROM users WHERE email = %s", email)
        user = cursor.fetchall()
    con.commit()
    con.close()
    return user

def autenticateUser(email, password):
    hashPassword = hashlib.md5(password.encode('utf-8')).hexdigest()
    con = obtain_connection()
    user = []
    with con.cursor() as cursor:
        cursor.execute("SELECT id, email, name, password FROM users WHERE email = %s AND password = %s", (email, hashPassword))
        user = cursor.fetchall()
    con.commit()
    con.close()
    return user
    
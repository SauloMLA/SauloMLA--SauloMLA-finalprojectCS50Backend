from bd import obtain_connection

def create_note(title, category, done, userId):
    con = obtain_connection()
    with con.cursor() as cursor:
        cursor.execute("INSERT INTO notes (title, category, done, userId) VALUES (%s, %s, %s, %s)", (title, category, done, userId))
    con.commit()
    con.close()

def get_notes(userId):
    con = obtain_connection()
    notes = []
    with con.cursor() as cursor:
        cursor.execute("SELECT id, title, category, done FROM notes WHERE userId = %s", (userId))
        notes = cursor.fetchall()
    con.close()
    return notes

def get_notes_by_category(category):
    con = obtain_connection()
    notes = []
    with con.cursor() as cursor:
        cursor.execute("SELECT id, title, category, done FROM notes WHERE category = %s", (category))
        notes = cursor.fetchall()
    con.close()
    return notes

def get_categories(userId):
    con = obtain_connection()
    categories = []
    with con.cursor() as cursor:
        cursor.execute("SELECT DISTINCT category FROM notes WHERE userId = %s", (userId))
        notes = cursor.fetchall()
    con.close()
    return notes

def delete_note(id):
    con = obtain_connection()
    with con.cursor() as cursor:
        cursor.execute(
            "DELETE FROM notes WHERE id = %s", (id))
    con.commit()
    con.close()

def update_note(id, title, category, done):
    con = obtain_connection()
    with con.cursor() as cursor:
        cursor.execute("UPDATE notes SET title = %s, category = %s, done = %s WHERE id = %s", (title, category, done, id))
    con.commit()
    con.close()

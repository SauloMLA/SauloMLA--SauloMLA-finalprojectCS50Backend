from flask import Flask, jsonify, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import re
import controllerNote
import controllerUsers
app = Flask(__name__)

app.config.from_object(__name__)
app.secret_key = '12345678'
app.config['PYTHONHASHSEED'] = 0

CORS(app, resources={r"/*":{'origins':"*"}})
CORS(app, resources={r"/*":{'origins':'http://localhost8000', "allow_headers": "Access-Control-Allow-Origin"}})


@app.route('/', methods=['GET'])
def greetings():
    return("Hello, world!")

@app.route('/login', methods=['GET', 'POST'])
def login():
    response_object = {'status': 'success'}
    if request.method == "POST":
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')
        user = controllerUsers.autenticateUser(email, password)
        if(len(user) < 1):
            response_object = {'status': 'error'}
            response_object['error'] = 'Email o contraseña incorrecto'
            return jsonify(response_object)
        else:
            return jsonify(user)
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    response_object = {'status': 'success'}
    if request.method == "POST":
        post_data = request.get_json()
        name = post_data.get('name')
        email = post_data.get('email')
        password = post_data.get('password')
        user = controllerUsers.get_userByEmail(email)
        if len(user) >= 1:
           response_object = {'status': 'error'}
           response_object['error'] = 'Email Already Used'
           return jsonify(response_object)
        controllerUsers.create_user(email, name, password)
        response_object['message'] = 'User Saved!'
        user = controllerUsers.autenticateUser(email, password)
        response_object['user'] = user
        return jsonify(response_object)
    else:
        return("Hello, register!")

@app.route('/notes', methods=['GET', 'POST'])
def all_notes():
    response_object = {'status': 'success'}
    if request.method == "POST":
        post_data = request.get_json()
        title = post_data.get('title')
        category = post_data.get('category')
        done = post_data.get('done')
        userId = post_data.get('userId')
        controllerNote.create_note(title, category, done, userId)
        response_object['message'] = 'Note Saved!'
    else:
        userId = request.args.get("userId", "")
        response_object['notes'] = controllerNote.get_notes(userId)
    return jsonify(response_object)

@app.route('/categories', methods=['GET', 'POST'])
def all_categories():
    response_object = {'status': 'success'}
    if request.method == "POST":
        post_data = request.get_json()
        category = post_data.get('category')
        response_object['notes'] = controllerNote.get_notes_by_category(category)
    userId = request.args.get("userId", "")
    response_object['categories'] = controllerNote.get_categories(userId)
    return jsonify(response_object)

@app.route('/notes/<note_id>', methods=['PUT', 'DELETE'])
def single_note(note_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        title = post_data.get('title')
        category = post_data.get('category')
        done = post_data.get('done')
        controllerNote.update_note(note_id, title, category, done)
        response_object['message'] = 'Note Updated!'
    if request.method == "DELETE":
        remove_note(note_id)
        response_object['message'] = 'Note removed!'    
    return jsonify(response_object)

def remove_note(note_id):
    controllerNote.delete_note(note_id)
    return True


if __name__ == "__main__":
    app.run(debug=True)

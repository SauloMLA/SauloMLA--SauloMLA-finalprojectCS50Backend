from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})
CORS(app, resources={r"/*":{'origins':'http://localhost8000', "allow_headers": "Access-Control-Allow-Origin"}})

@app.route('/', methods=['GET'])
def greetings():
    return("Hello, world!")

@app.route('/shark', methods=['GET'])
def shark():
    return("Shark")

NOTES = [
    {
        'id': uuid.uuid4().hex,
        'title': 'Math Homework',
        'category': 'School',
        'done': False,
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Redisign banner',
        'category': 'Work',
        'done': False,
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Wash dishes',
        'category': 'Home',
        'done': False,
    },
]

@app.route('/notes', methods=['GET', 'POST'])
def all_notes():
    response_object = {'status': 'success'}
    if request.method == "POST":
        post_data = request.get_json()
        NOTES.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'category': post_data.get('category'),
            'done': post_data.get('done'),
        })
        response_object['message'] = 'Note Saved!'
    else:
        response_object['notes'] = NOTES
    return jsonify(response_object)

@app.route('/notes/<note_id>', methods=['PUT', 'DELETE'])
def single_note(note_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_note(note_id)
        NOTES.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'category': post_data.get('category'),
            'done': post_data.get('done'),
        })
        response_object['message'] = 'Note Updated!'
    if request.method == "DELETE":
        remove_note(note_id)
        response_object['message'] = 'Note removed!'    
    return jsonify(response_object)

def remove_note(note_id):
    for note in NOTES:
        if note['id'] == note_id:
            NOTES.remove(note)
            return True
    return False


if __name__ == "__main__":
    app.run(debug=True)

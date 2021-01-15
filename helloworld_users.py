from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import random
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

users = {
    'users_list':
    [
        {
            'id': 'xyz789',
            'name': 'Charlie',
            'job': 'Janitor',
        },
        {
            'id':'abc123',
            'name': 'Mac',
            'job': 'Bouncer',
        },
        {
            'id': 'ppp222',
            'name': 'Mac',
            'job': 'Professor',
        },
        {
            'id': 'yat999',
            'name': 'Dee',
            'job': 'Aspiring actress',
        },
        {
            'id': 'zap555',
            'name': 'Dennis',
            'job': 'Bartender',
        }
    ]
}

def generateID():
    id = ""
    for i in range(3):
        id = id + str(chr(random.randint(97, 122)))
    for i in range(3):
        id = id + str(random.randint(0, 9))
    return id

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def get_users():
    if request.method == 'GET':
        search_job = request.args.get('job')
        flag = False
        if search_job:
            flag = True
        
        search_username = request.args.get('name')  # accessing the value of parameter 'name'
        if search_username:
            subdict = {'users_list': []}
            for user in users['users_list']:
                if (flag and (user['name'] == search_username) and (user['job'] == search_job)):
                    subdict['users_list'].append(user)
                elif ((not flag) and (user['name'] == search_username)):
                    subdict['users_list'].append(user)
            return subdict
        return users
    elif request.method == 'POST':
        userToAdd = request.get_json()
        userToAdd['id'] = generateID()
        users['users_list'].append(userToAdd)
        resp = jsonify(success=True)
        resp.status_code = 201
        # optionally, you can always set a response code
        # 200 is the default code for a normal response
        return resp
    elif request.method == 'DELETE':
        user_del = request.get_json()
        subdict = {'users_list': []}
        for user in users['users_list']:
            if user != user_del:
                subdict['users_list'].append(user)
        users['users_list'] = subdict['users_list']
        resp = jsonify(success=True)
        return resp

@app.route('/users/<id>')
def get_user(id):
    if id:
        for user in users['users_list']:
            if user['id'] == id:
                return user
        return ({})
    return users
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import json
#import random
from model_mongodb import User

app = Flask(__name__)
# CORS stands for Cross Origin Requests.
# Here we'll allow requests coming from any domain. Not recommended for production environment.
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

users = {
    'users_list': []
}

#def generateID():
#    id = ""
#    for i in range(3):
#        id = id + str(chr(random.randint(97, 122)))
#    for i in range(3):
#        id = id + str(random.randint(0, 9))
#    return id

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def get_users():
    if request.method == 'GET':
        search_username = request.args.get('name')
        search_job = request.args.get('job')
        if search_username and search_job:
            users = User().find_by_name_job(search_username, search_job)
        elif search_username:
            users = User().find_by_name(search_username)
        elif search_job:
            return find_users_by_job(search_job)
        else:
            users = User().find_all()
        return {"users_list": users}
    elif request.method == 'POST':
        userToAdd = request.get_json()
        #userToAdd['id'] = generateID()
        #users['users_list'].append(userToAdd)
        newUser = User(userToAdd)
        newUser.save()
        resp = jsonify(newUser), 201
        # optionally, you can always set a response code
        # 200 is the default code for a normal response
        return resp
    elif request.method == 'DELETE':
        user_del = request.get_json()
        delUser = User(user_del)
        resp = jsonify(delUser.remove()), 200
        #users['users_list'].remove(user_del)
        #resp = jsonify(success=True)
        #resp.status_code = 200
        return resp

@app.route('/users/<id>')
def get_user(id):
    if request.method == 'GET':
        user = User({"_id":id})
        if user.reload():
            return user
        else:
            return jsonify({"error": "User not found"}), 404

#def find_users_by_name_job(name, job):
#    subdict = {'users_list': []}
#    for user in users['users_list']:
#        if user['name'] == name and user['job'] == job:
#            subdict['users_list'].append(user)
#    return subdict

def find_users_by_job(job):
    subdict = {'users_list': []}
    for user in users['users_list']:
        if user['job'] == job:
            subdict['users_list'].append(user)
    return subdict
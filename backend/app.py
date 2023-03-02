from flask import Flask, redirect, render_template, request, jsonify, Response, session, url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash
from bson import json_util
from bson.objectid import ObjectId


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/Green"


mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create_user():
    #receive data !
    # print(request.json)
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and email and password:
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert_one(
            {'username': username, 'email': email, 'password': hashed_password}
        )
        response = {
            '_id': str(id),
            'username': username,
            'password': hashed_password,
            'email': email
        }
        return response
    else:
        return not_found()
            


    return {'message': 'received'}

@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    # print(id)
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response

@app.route('/users/<_id>', methods=['PUT'])
def update_user(_id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    if username and email and password and _id:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'username': username, 'email': email, 'password': hashed_password}})
        response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()


@app.errorhandler(404)
def not_found(error = None):
    response = jsonify({
        'message': 'Resource Not Found' + request.url,
        'status': 404
    })
    
    response.status_code = 404
    return response

# @app.route('/regsiter', methods = ['POST', 'GET'])
# def regsiter():
    # username = request.form['username']
    # password = request.form['password']
    # email = request.form['email']

    # if request.method == 'POST':
    #     users = mongo.db.users
    #     existing_user = users.find_one({'name' : request.form['username']})
    #     if existing_user is None:
    #         hashed_password = generate_password_hash(request.form['password'])
    #         id = mongo.db.users.insert_one(
    #          {'username': request.form['username'], 'email': request.form['email'], 'password': hashed_password}
    #         )
    #         return redirect(url_for('index'))
    # else:
    #     render_template('registration.html')




    # if  username and email and password:
    #     hashed_password = generate_password_hash(password)
    #     id = mongo.db.users.insert_one(
    #         {'username': username, 'email': email, 'password': hashed_password}
    #     )
    #     response = {
    #         '_id': str(id),
    #         'username': username,
    #         'password': hashed_password,
    #         'email': email
    #     }
    #     return jsonify(response)
    # else:
    #     # Return error message
    #     return jsonify({'message': 'All fields are required'})
    

if __name__ == '__main__':
    app.run(debug=True)
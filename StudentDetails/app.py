from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from student import Student, StudentList
from user import UserRegister

app = Flask(__name__)
api = Api(app)
app.secret_key = "bottle"

jwt = JWT(app, authenticate, identity)

api.add_resource(Student, '/students/<string:name>')
api.add_resource(StudentList, '/students')
api.add_resource(UserRegister, '/userRegister')


if __name__ == "__main__":
    app.run(port=5555,debug=True)

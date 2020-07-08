from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.student import Student, StudentList
from resources.user import UserRegister
from resources.departments import Department, DepartmentList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studentDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
app.secret_key = "bottle"

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Student, '/students/<string:name>')
api.add_resource(Department, '/departments/<string:name>')
api.add_resource(StudentList, '/students')
api.add_resource(DepartmentList, '/departments')
api.add_resource(UserRegister, '/userRegister')


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5555,debug=True)

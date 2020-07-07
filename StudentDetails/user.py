import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls,usename):
        connection = sqlite3.connect("studentDB.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query,(usename,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect("studentDB.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", required=True, type=str, help="Please enter a username")
    parser.add_argument("password", required=True, type=str, help="Please enter password")

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "Username already exists!"}, 400

        connection = sqlite3.connect("studentDB.db")
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL,?,?)"
        cursor.execute(query,(data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message":"User created successfully."}, 201
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

#from security import authenticate, identity
from resources.student import Student, StudentList
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.departments import Department, DepartmentList
from db import db
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studentDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']
api = Api(app)
app.secret_key = "bottle"

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def is_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description':'The token has expired',
        'error':'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify({
        'description':'Signature verification failed',
        'error':'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback():
    return jsonify({
        'description':'Request doen not contain an access token',
        'error':'authorisation_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description':'The token is not fresh',
        'error':'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description':'The token has been revoked',
        'error':'token_revoked'
    }), 401

api.add_resource(Student, '/students/<string:name>')
api.add_resource(Department, '/departments/<string:name>')
api.add_resource(StudentList, '/students')
api.add_resource(DepartmentList, '/departments')
api.add_resource(UserRegister, '/userRegister')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5555,debug=True)

from flask_restful import Resource
from flask_jwt import jwt_required
from models.departments import DepartmentModel

class Department(Resource):

    @jwt_required()
    def get(self, name):
        department = DepartmentModel.find_by_name(name)
        if department:
            return department.json()
        return {"message":"Department not found"},404

    def post(self, name):

        department = DepartmentModel.find_by_name(name)
        if department:
            return {"message": "A department with name {} already exists.".format(name)}, 400

        department = DepartmentModel(name)
        try:
            department.save_to_db()
        except:
            return {"message":"An error occurred while inserting the details."}, 500
        return {"message":"Department added successfully","Department":department.json()}, 201

    def delete(self, name):
        department = DepartmentModel.find_by_name(name)
        if department:
            department.delete_from_db()
            return {"message": "Department deleted!"}
        return {"message":"Department not found"},404


class DepartmentList(Resource):
    def get(self):
        return {"Departments": [department.json() for department in DepartmentModel.query.all()]}

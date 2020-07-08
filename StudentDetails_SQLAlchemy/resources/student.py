from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.student import StudentModel

class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("cgpa", required=True, type=float, help="This filed cant be left empty")
    parser.add_argument("department_id", required=True, type=int, help="Student's registered department")

    @jwt_required()
    def get(self, name):
        student = StudentModel.find_by_name(name)
        if student:
            return {"Student Details": student.json()}
        return {"message":"Student not found"},404

    def post(self, name):

        student = StudentModel.find_by_name(name)
        if student:
            return {"message": "A student with name {} already exists.".format(name)}, 400

        data = Student.parser.parse_args()
        student = StudentModel(name, **data)
        try:
            student.save_to_db()
        except:
            return {"message":"An error occurred while inserting the details."}, 500
        return {"message":"Student details added successfully","Student Details":student.json()}, 201

    def delete(self, name):
        student = StudentModel.find_by_name(name)
        if student:
            student.delete_from_db()
            return {"message": "Student details deleted!"}
        return {"message":"Student not found"},404

    def put(self, name):
        data = Student.parser.parse_args()
        student = StudentModel.find_by_name(name)
        if student:
            student.cgpa = data['CGPA']
        else:
            student = StudentModel(name, **data)

        student.save_to_db()

        return student.json()



class StudentList(Resource):
    def get(self):
        return {"Students": [student.json() for student in StudentModel.query.all()]}

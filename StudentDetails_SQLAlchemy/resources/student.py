from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity, fresh_jwt_required
from models.student import StudentModel

class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("cgpa", required=True, type=float, help="This filed cant be left empty")
    parser.add_argument("department_id", required=True, type=int, help="Student's registered department")

    @jwt_required
    def get(self, name):
        student = StudentModel.find_by_name(name)
        if student:
            return {"Student Details": student.json()}
        return {"message":"Student not found"},404

    @fresh_jwt_required
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

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message": "Admin privileges required "}, 401
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
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        student_list = [student.json() for student in StudentModel.find_all()]
        if user_id:
            return {"Students": student_list}, 200

        return {"names": [student['name'] for student in student_list],
                "message": "Please log in for more information"}, 200


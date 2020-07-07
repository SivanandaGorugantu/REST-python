from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("CGPA", required=True, type=float, help="This filed cant be left empty")

    @jwt_required()
    def get(self, name):
        student = self.find_by_name(name)
        if student:
            return student
        return {"message":"Student not found"},404

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect("studentDB.db")
        cursor = connection.cursor()

        query = "SELECT * FROM students WHERE name=?"
        result = cursor.execute(query, (name,))

        row = result.fetchone()
        connection.close()

        if row:
            return {"Student Details": {"name": row[0], "CGPA": row[1]}}


    def post(self, name):

        student = self.find_by_name(name)
        if student:
            return {"message": "A student with name {} already exists.".format(name)}, 400

        data = Student.parser.parse_args()
        student = {'name':name,"CGPA":data['CGPA']}
        try:
            self.insert(student)
        except:
            return {"message":"An error occurred while inserting the details."}, 500
        return {"message":"Student details added successfully","Student Details":student}, 201


    @classmethod
    def insert(cls,student):
        connection = sqlite3.connect("studentDB.db")
        cursor = connection.cursor()

        insert_query = "INSERT INTO students VALUES (?,?)"

        cursor.execute(insert_query, (student['name'], student['CGPA']))

        connection.commit()
        connection.close()

    def delete(self, name):
        student = self.find_by_name(name)
        if student:
            connection = sqlite3.connect("studentDB.db")
            cursor = connection.cursor()

            query = "DELETE FROM students WHERE name=?"

            cursor.execute(query,(name,))
            connection.commit()
            connection.close()
            return {"message": "Student details deleted!"}
        return {"message":"Student not found"},404

    def put(self, name):
        data = Student.parser.parse_args()
        student_update = {'name': name, 'CGPA': data['CGPA']}

        student = self.find_by_name(name)
        if student:
            try:
                self.update(student_update)
            except:
                return {"message": "An error occurred while updating the details."}, 500

        else:
            try:
                self.insert(student_update)
            except:
                return {"message": "An error occurred while inserting the details."}, 500

        return student_update

    @classmethod
    def update(cls,student):
        connection = sqlite3.connect("studentDB.db")
        cursor = connection.cursor()

        query = "UPDATE students SET CGPA=? WHERE name=?"

        cursor.execute(query,(student['CGPA'],student['name']))
        connection.commit()
        connection.close()


class StudentList(Resource):
    def get(self):
        connection = sqlite3.connect("studentDB.db")
        cursor = connection.cursor()
        query = "SELECT * FROM students"

        all_students = []
        for row in cursor.execute(query):
            all_students.append({"name":row[0],"CGPA":row[1]})

        connection.close()
        return {"Students": all_students}

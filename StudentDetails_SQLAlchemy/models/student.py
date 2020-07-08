from db import db

class StudentModel(db.Model):

    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    cgpa = db.Column(db.Float(precision=2))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    department = db.relationship('DepartmentModel')

    def __init__(self,name,cgpa,department_id):
        self.name = name
        self.cgpa = cgpa
        self.department_id = department_id

    def json(self):
        return {"name":self.name, "CGPA":self.cgpa, "department_id":self.department_id}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
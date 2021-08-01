from db import db
from datetime import datetime


class EmployeeModel(db.Model):
	__tablename__ = "employees"

	employee_id = db.Column(db.Integer, primary_key=True)
	last_name = db.Column(db.String(40), nullable=False)
	first_name = db.Column(db.String(40), nullable=False)
	birth_date = db.Column(db.Date, default=datetime.utcnow)
	photo = db.Column(db.String(20), default='abc')
	notes = db.Column(db.String(100), default='abc')

	orders = db.relationship('OrderModel', backref='employee')
	
	def __init__(self, last_name, first_name, birth_date, photo, notes):
		self.last_name = last_name
		self.first_name = first_name
		self.birth_date = birth_date
		self.photo = photo
		self.notes = notes
		
	def json(self):
		return {
			"employee_id" : self.employee_id,
			"last_name" : self.last_name,
			"first_name" : self.first_name,
			"birth_date" : self.birth_date.__str__(),
			"photo" : self.photo,
			"notes" : self.notes
		}

	@classmethod
	def find_by_employee_name(cls, last_name):
		return cls.query.filter_by(last_name = last_name).first()
	
	@classmethod
	def find_by_employee_id(cls, employee_id):
		return cls.query.filter_by(employee_id = employee_id).first()
	
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
	
	def update_from_db(self, first_name, birth_date, photo, notes):
		self.first_name = first_name
		self.birth_date = birth_date
		self.photo = photo
		self.notes = notes
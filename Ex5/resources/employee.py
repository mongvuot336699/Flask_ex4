from flask_restful import Resource, reqparse
from models.employee import EmployeeModel
from datetime import datetime


class Employee(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('first_name',
						type=str,
						required=True,
						help="This field cannot be empty")
	parser.add_argument('birth_date',
						type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
						required=True,
						help="This field cannot be empty")
	parser.add_argument('photo',
						type=str,
						required=True,
						help="This field cannot be empty")
	parser.add_argument('notes',
						type=str,
						required=True,
						help="This field cannot be empty")

	def get(self, last_name):
		employee = EmployeeModel.find_by_employee_name(last_name)
		if employee:
			return employee.json()
		return {'message': 'Employee not found'}, 404

	def post(self, last_name):
		if EmployeeModel.find_by_employee_name(last_name):
			return {'message': 'The Employee with last name {} already exists.'.format(last_name)}, 400
		
		data = Employee.parser.parse_args()

		employee = EmployeeModel(last_name, **data)

		try:
			employee.save_to_db()
		except:
			return {"message": "An error occurred when inserting employee"}, 500
		
		return employee.json(), 201

	def delete(self, last_name):
		employee = EmployeeModel.find_by_employee_name(last_name)
		if employee:
			employee.delete_from_db()
			return {'message': 'Employee deleted'}
		return {'message': 'Employee not found'}, 404
	
	def put(self, last_name):
		data = Employee.parser.parse_args()
		employee = EmployeeModel.find_by_employee_name(last_name)
		
		if employee:
			employee.update_from_db(**data)
		else:
			employee = EmployeeModel(last_name, **data)

		employee.save_to_db()
		
		return employee.json()

class EmployeeList(Resource):
	def get(self):
		return {'employees': [employee.json() for employee in EmployeeModel.query.all()]}
	
	
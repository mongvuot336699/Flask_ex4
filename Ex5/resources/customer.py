from flask_restful import Resource, reqparse
from models.customer import CustomerModel


class Customer(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('contact_name',
						type=str,
						required=True,
						help="This field cannot be empty")
	parser.add_argument('address',
						type=str,
						required=True,
						help="This field cannot be empty")
	parser.add_argument('city',
						type=str,
						required=True,
						help="This field cannot be empty")
	parser.add_argument('postal_code',
						type=str,
						required=True,
						help="This field cannot be empty")
	parser.add_argument('country',
						type=str,
						required=True,
						help="This field cannot be empty")

	def get(self, customer_name):
		customer = CustomerModel.find_by_customer_name(customer_name)
		if customer:
			return customer.json()
		return {'message': 'Customer not found'}, 404

	def post(self, customer_name):
		if CustomerModel.find_by_customer_name(customer_name):
			return {'message': 'The Customer with name {} already exists.'.format(customer_name)}, 400
		
		data = Customer.parser.parse_args()

		customer = CustomerModel(customer_name, **data)

		try:
			customer.save_to_db()
		except:
			return {"message": "An error occurred when inserting customer"}, 500
		
		return customer.json(), 201

	def delete(self, customer_name):
		customer = CustomerModel.find_by_customer_name(customer_name)
		if customer:
			customer.delete_from_db()
			return {'message': 'Customer deleted'}
		return {'message': 'Customer not found'}, 404
	
	def put(self, customer_name):
		data = Customer.parser.parse_args()
		customer = CustomerModel.find_by_customer_name(customer_name)
		
		if customer:
			customer.update_from_db(**data)
		else:
			customer = CustomerModel(customer_name, **data)

		customer.save_to_db()
		
		return customer.json()

class CustomerList(Resource):
	def get(self):
		return {'customers': [customer.json() for customer in CustomerModel.query.all()]}
	
	
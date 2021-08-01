from flask_restful import Resource, reqparse
from datetime import datetime

from models.order import OrderModel
from models.employee import EmployeeModel
from models.customer import CustomerModel
from models.shipper import ShipperModel


class Order(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('order_id',
						type=int,
						required=False)
	parser.add_argument('customer_id',
						type=int,
						required=True,
						help="This field cannot be empty")
	parser.add_argument('employee_id',
						type=int,
						required=True,
						help="This field cannot be empty")
	parser.add_argument('order_date',
						type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
						required=True,
						help="This field cannot be empty")
	parser.add_argument('shipper_id',
						type=int,
						required=True,
						help="This field cannot be empty")

	def get(self):
		if Order.parser.parse_args()['order_id']:
			id = Order.parser.parse_args()['order_id']
			order = OrderModel.find_by_order_id(id)
			if order:
				return order.json()
			return {'message': 'Order not found'}, 404
		else:
			return {'message': 'Order ID not found'}, 400

	def post(self):
		data = Order.parser.parse_args()
		del data['order_id']
		customer = CustomerModel.find_by_customer_id(data['customer_id'])
		if(not customer):
			return {'message': 'Customer ID not found'}, 404
		
		employee = EmployeeModel.find_by_employee_id(data['employee_id'])
		if(not employee):
			return {'message': 'Employee ID not found'}, 404

		shipper = ShipperModel.find_by_shipper_id(data['shipper_id'])
		if(not shipper):
			return {'message': 'Shipper ID not found'}, 404

		order = OrderModel(**data)
		try:
			order.save_to_db()
		except:
			return {"message": "An error occurred when inserting shipper"}, 500
		
		return order.json(), 201

	def delete(self):
		if Order.parser.parse_args()['order_id']:
			id = Order.parser.parse_args()['order_id']
			order = OrderModel.find_by_order_id(id)
			if order:
				order.delete_from_db()
				return {'message': 'Order deleted'}
			return {'message': 'Order not found'}, 404
		else:
			return {'message': 'Order ID not found'}, 400
	
	def put(self, shipper_name):
		data = Order.parser.parse_args()

		if Order.parser.parse_args()['order_id']:
			id = Order.parser.parse_args()['order_id']
			customer = CustomerModel.find_by_customer_id(data['customer_id'])
			if(not customer):
				return {'message': 'Customer ID not found'}, 404
		
			employee = EmployeeModel.find_by_employee_id(data['employee_id'])
			if(not employee):
				return {'message': 'Employee ID not found'}, 404

			shipper = ShipperModel.find_by_shipper_id(data['shipper_id'])
			if(not shipper):
				return {'message': 'Shipper ID not found'}, 404

			order = OrderModel.find_by_order_id(id)
			if order:
				order.update_from_db(**data)
			else:
				order = OrderModel(**data)

			order.save_to_db()
		
			return order.json()
		else:
			return {'message': 'Order ID not found'}, 400

class OrderList(Resource):
	def get(self):
		return {'orders': [order.json() for order in OrderModel.query.all()]}
	
	
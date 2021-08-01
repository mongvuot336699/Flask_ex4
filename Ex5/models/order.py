from db import db
from datetime import datetime


class OrderModel(db.Model):
	__tablename__ = "orders"

	order_id = db.Column(db.Integer, primary_key=True)
	customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
	employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)
	order_date = db.Column(db.DateTime, nullable=False)
	shipper_id = db.Column(db.Integer, db.ForeignKey('shippers.shipper_id'), nullable=False)
	
	def __init__(self, customer_id, employee_id, order_date, shipper_id):
		self.customer_id = customer_id
		self.employee_id = employee_id
		self.order_date = order_date
		self.shipper_id = shipper_id
		
	def json(self):
		return {
			"order_id" : self.order_id,
			"customer_id" : self.customer_id,
			"employee_id" : self.employee_id,
			"order_date" : self.order_date.__str__(),
			"shipper_id" : self.shipper_id
		}

	@classmethod
	def find_by_order_id(cls, _id):
		return cls.query.filter_by(order_id = _id).first()
	
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
	
	def update_from_db(self, customer_id, employee_id, order_date, shipper_id):
		self.customer_id = customer_id
		self.employee_id = employee_id
		self.order_date = order_date
		self.shipper_id = shipper_id
		self.customer = customer 
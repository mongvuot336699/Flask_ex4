from db import db


class CustomerModel(db.Model):
	__tablename__ = "customers"

	customer_id = db.Column(db.Integer, primary_key=True)
	customer_name = db.Column(db.String(40))
	contact_name = db.Column(db.String(40))
	address = db.Column(db.String(40))
	city = db.Column(db.String(20))
	postal_code = db.Column(db.String(10))
	country = db.Column(db.String(20))

	orders = db.relationship('OrderModel', backref='customer')

	def __init__(self, customer_name, contact_name, address, city, postal_code, country):
		self.customer_name = customer_name
		self.contact_name = contact_name
		self.address = address
		self.city = city
		self.postal_code = postal_code
		self.country = country

	def json(self):
		return {
			"customer_id" : self.customer_id,
			"customer_name" : self.customer_name,
			"contact_name" : self.contact_name,
			"address" : self.address,
			"city" : self.city,
			"postal_code" : self.postal_code,
			"country" : self.country
		}

	@classmethod
	def find_by_customer_name(cls, customer_name):
		return cls.query.filter_by(customer_name = customer_name).first()
	
	@classmethod
	def find_by_customer_id(cls, customer_id):
		return cls.query.filter_by(customer_id = customer_id).first()
	
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
	
	def update_from_db(self, contact_name, address, city, postal_code, country):
		self.contact_name = contact_name
		self.address = address
		self.city = city
		self.postal_code = postal_code
		self.country = country
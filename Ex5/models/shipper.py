from db import db
from datetime import datetime


class ShipperModel(db.Model):
	__tablename__ = "shippers"

	shipper_id = db.Column(db.Integer, primary_key=True)
	shipper_name = db.Column(db.String(40), nullable=False)
	phone = db.Column(db.String(20), nullable=False)

	orders = db.relationship('OrderModel', backref='shipper')
	
	def __init__(self, shipper_name, phone):
		self.shipper_name = shipper_name
		self.phone = phone
		
	def json(self):
		return {
			"shipper_id" : self.shipper_id,
			"shipper_name" : self.shipper_name,
			"phone" : self.phone
		}

	@classmethod
	def find_by_shipper_name(cls, shipper_name):
		return cls.query.filter_by(shipper_name = shipper_name).first()
	
	@classmethod
	def find_by_shipper_id(cls, shipper_id):
		return cls.query.filter_by(shipper_id = shipper_id).first()
	
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
	
	def update_from_db(self, phone):
		self.phone = phone
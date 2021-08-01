from flask_restful import Resource, reqparse
from models.shipper import ShipperModel
from datetime import datetime


class Shipper(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('phone',
						type=str,
						required=True,
						help="This field cannot be empty")

	def get(self, shipper_name):
		shipper = ShipperModel.find_by_shipper_name(shipper_name)
		if shipper:
			return shipper.json()
		return {'message': 'Shipper not found'}, 404

	def post(self, shipper_name):
		if ShipperModel.find_by_shipper_name(shipper_name):
			return {'message': 'The Shipper with name {} already exists.'.format(shipper_name)}, 400
		
		data = Shipper.parser.parse_args()

		shipper = ShipperModel(shipper_name, **data)

		try:
			shipper.save_to_db()
		except:
			return {"message": "An error occurred when inserting shipper"}, 500
		
		return shipper.json(), 201

	def delete(self, shipper_name):
		shipper = ShipperModel.find_by_shipper_name(shipper_name)
		if shipper:
			shipper.delete_from_db()
			return {'message': 'Shipper deleted'}
		return {'message': 'Shipper not found'}, 404
	
	def put(self, shipper_name):
		data = Shipper.parser.parse_args()
		shipper = ShipperModel.find_by_shipper_name(shipper_name)
		
		if shipper:
			shipper.update_from_db(**data)
		else:
			shipper = ShipperModel(shipper_name, **data)

		shipper.save_to_db()
		
		return shipper.json()

class ShipperList(Resource):
	def get(self):
		return {'shippers': [shipper.json() for shipper in ShipperModel.query.all()]}
	
	
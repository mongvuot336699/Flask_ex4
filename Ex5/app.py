from flask import Flask
from flask_restful import Api
from db import db

from resources.customer import Customer, CustomerList
from resources.employee import Employee, EmployeeList
from resources.shipper import Shipper, ShipperList
from resources.order import Order, OrderList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def create_tables():
	db.create_all()

api.add_resource(Customer, '/customer/<string:customer_name>')
api.add_resource(CustomerList, '/customers')
api.add_resource(Shipper, '/shipper/<string:shipper_name>')
api.add_resource(ShipperList, '/shippers')
api.add_resource(Employee, '/employee/<string:last_name>')
api.add_resource(EmployeeList, '/employees')
api.add_resource(Order, '/order')
api.add_resource(OrderList, '/orders')
# api.add_resource(Order, '/order/<string:order_id>')

if __name__ == '__main__':
	db.init_app(app)
	app.run(port=5000, debug=True)
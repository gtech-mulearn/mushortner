from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@localhost/mu_dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)




class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, World!'}

    def post(self):
        data = request.get_json()
        name = data['name']
        return {'message': f'Hello, {name}!'}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)

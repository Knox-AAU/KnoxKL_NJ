from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Triple_test(Resource):
    def post(self):
        return 'returned content: <{}>'.format(str(request.data.decode('utf-8')))

api.add_resource(Triple_test, '/update') # Endpoint


if __name__ == '__main__':
     app.run(port='53254')
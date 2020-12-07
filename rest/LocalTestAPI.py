from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Triple_test(Resource):
    def post(self):
        return 'returned content: <{}>'.format(str(request.data.decode('utf-8')))

class Word_count_test(Resource):
    def post(self):
        data = str(request.data.decode('utf-8'))
        print(f'Received data: <{data}>')
        return 'Received word_count OK'

api.add_resource(Triple_test, '/update') # Endpoint
api.add_resource(Word_count_test, '/wordCountData')


if __name__ == '__main__':
     app.run(port='53253')
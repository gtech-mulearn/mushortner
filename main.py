from flask import Flask, redirect
from flask_restful import Resource, Api

from models.connection import DBConnection

app = Flask(__name__)
api = Api(app)
db = DBConnection()


class UrlShortnerAPI(Resource):
    def get(self, short_url):
        query = "SELECT long_url FROM `url_shortener` where short_url = :short_url; "
        params = {'short_url': short_url}
        url = db.fetch_single_data(query, params)
        if url:
            return redirect(url)
        return {
            "hasError": True,
            "statusCode": 400,
            "message": "Url Not Found",
            "response": {}
        }


api.add_resource(UrlShortnerAPI, '/get/<string:short_url>/')

if __name__ == '__main__':
    app.run(debug=True)

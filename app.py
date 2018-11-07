from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from resources.scraper import Scraper
from flask_restful.utils import cors

app = Flask(__name__)
api = Api(app)
app.config.from_object('config')

app.secret_key = "WDn865s1021"

#CORS(app)
#cors = CORS(app, resources={r"/auth": {"origins": "*"}})
app.config['DEBUG'] = True

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, origin, accept')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

api.add_resource(Scraper,'/<string:data>')

if __name__ == '__main__':    

    app.run(port=5000)

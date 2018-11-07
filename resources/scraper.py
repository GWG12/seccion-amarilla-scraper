import flask
from flask_restful import Resource, reqparse
from models.scraper import ScraperModel
import urllib
import json
from flask import Response


class Scraper(Resource):

    def get(self,data):
        search_term = urllib.parse.unquote(data)
        if '+' in search_term:
            search_term = search_term.replace('+',' ')        
        parser = ScraperModel(search_term)
        csv = parser.compiling()
        #response = flask.make_response(csv)
        #response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        #response.headers['content-type'] = 'application/octet-stream'
        #response.headers["Content-Type"] = "text/csv"
        #csv = '1,2,3\n4,5,6\n'
        response = Response(csv, mimetype='text/csv')
        response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
        try:
            #return json.loads(response)
            return response
        except:
            return {"error":"Hubo un error en el servidor"},500

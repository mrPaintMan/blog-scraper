from flask_restful import Resource
from flask import request
import requests


class Ci(Resource):

    @staticmethod
    def post():
        url = "http://jenkins:kallekula@192.168.0.100:8080/github-webhook/"
        response = requests.post(url, headers=request.headers, json=request.json)

        return {"status": f"{response.content}"}, response.status_code

    @staticmethod
    def get():
        return {"status": "404 - Resource not found."}, 404

    @staticmethod
    def put():
        return {"status": "404 - Resource not found."}, 404

    @staticmethod
    def delete():
        return {"status": "404 - Resource not found."}, 404

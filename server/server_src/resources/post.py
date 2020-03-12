from flask_restful import Resource
from flask import request
from server_src.lib.model import post_model
from server_src.lib.db import Db


class Post(Resource):

    @classmethod
    def setup(cls, host, auth):
        cls.db = Db(host)
        cls.decorators = [auth.login_required]
        return cls

    @staticmethod
    def post(post_id):
        return {"status": "404 - Resource not found."}, 404

    def get(self, post_id):
        try:
            p_id = int(post_id)
            if p_id < 1:
                raise ValueError

        except ValueError:
            return {
                       "status": "400 - Bad request.",
                       "error": "post_id is invalid. Should be: /posts/{int} and > 0"
                   }, 400

        except TypeError:

            return {
                       "status": "400 - Bad request.",
                       "error": "post_id is missing or invalid. Should be: /posts/{int} and > 0"
                   }, 400

        posts = post_model.get_by_id(self.db, p_id)

        return {
            "status": "200 - Ok",
            "data": posts
        }

    @staticmethod
    def put(post_id):
        return {"status": "404 - Resource not found."}, 404

    @staticmethod
    def delete(post_id):
        return {"status": "404 - Resource not found."}, 404


class PostList(Resource):

    @classmethod
    def setup(cls, host, auth):
        cls.db = Db(host)
        cls.decorators = [auth.login_required]
        return cls

    @staticmethod
    def post():
        return {"status": "404 - Resource not found."}, 404

    def get(self):

        try:
            page = int(request.args.get('page'))
            source = str(request.args.get('source'))
            if page < 0:
                raise ValueError

        except ValueError:
            return {
                       "status": "400 - Bad request.",
                       "error": "Pagination query parameter is invalid. Should be: ?page={int} and >= 0"
                   }, 400
        except TypeError:
            return {
                       "status": "400 - Bad request.",
                       "error": "Pagination query parameter is missing or invalid. Should be: ?page={int} and >= 0"
                   }, 400

        if source is not None and source != "None":
            posts = post_model.get_pag_by_source(self.db, page, source)

        else:
            posts = post_model.get_pag(self.db, page)

        return {
            "status": "200 - Ok",
            "data": posts
        }

    @staticmethod
    def put():
        return {"status": "404 - Resource not found."}, 404

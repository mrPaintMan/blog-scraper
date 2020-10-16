from flask_restful import Resource
from server_src.lib.model import source_model
from server_src.lib.db import Db


class Source(Resource):

    @classmethod
    def setup(cls, host, auth):
        cls.db = Db(host)
        cls.decorators = [auth.login_required]
        return cls

    def get(self, source_code):
        try:
            source = str(source_code)

        except ValueError:
            return {
                       "status": "400 - Bad request.",
                       "error": "source_code is missing or invalid. Should be: /sources/{string}"
                   }, 400

        posts = source_model.get_by_code(self.db, source)

        return {
            "status": "200 - Ok",
            "data": posts
        }


class SourceList(Resource):

    @classmethod
    def setup(cls, host, auth):
        cls.db = Db(host)
        cls.decorators = [auth.login_required]
        return cls

    def get(self):
        posts = source_model.get_all(self.db)

        return {
            "status": "200 - Ok",
            "data": posts
        }

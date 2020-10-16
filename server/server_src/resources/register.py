from flask_restful import Resource
from flask import request
from server_src.lib.db import Db
from server_src.lib.model.register_model import Registration


class Register(Resource):

    @classmethod
    def setup(cls, host, auth):
        cls.db = Db(host)
        cls.decorators = [auth.login_required]
        return cls

    def post(self):
        registrations = []
        existing_registrations = []
        obj = request.json

        if obj["source_codes"] is None:
            return {"status": "400 - Bad request"}, 400

        elif len(obj["source_codes"]) == 0:
            registration = Registration(None, obj["device_token"], None, None)
            existing_registrations = registration.get_by_device_token(self.db)

        for source in obj["source_codes"]:
            registration = Registration(None, obj["device_token"], source, None)
            registration.match(self.db)
            registration.save(self.db)
            registrations.append(registration)

            if obj["source_codes"].index(source) == len(obj["source_codes"]) - 1:
                existing_registrations = registration.get_by_device_token(self.db)

        for registration in existing_registrations:
            if registration.source_code not in obj["source_codes"]:
                registration.delete(self.db)

        return {"status": "200 - Ok"}

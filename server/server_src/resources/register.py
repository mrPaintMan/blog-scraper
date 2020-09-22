from flask_restful import Resource
from flask import request
from server_src.lib.db import Db
from server_src.lib.model.notification_model import Notification


class Register(Resource):

    @classmethod
    def setup(cls, host, auth):
        cls.db = Db(host)
        cls.decorators = [auth.login_required]
        return cls

    def post(self):
        notifications = []
        existing_notifications = []
        obj = request.json

        if obj["source_codes"] is None:
            return {"status": "400 - Bad request"}, 400

        elif len(obj["source_codes"]) == 0:
            notification = Notification(None, obj["device_token"], None, None)
            existing_notifications = notification.get_by_device_token(self.db)

        for source in obj["source_codes"]:
            notification = Notification(None, obj["device_token"], source, None)
            notification.match(self.db)
            notification.save(self.db)
            notifications.append(notification)

            if obj["source_codes"].index(source) == len(obj["source_codes"]) - 1:
                existing_notifications = notification.get_by_device_token(self.db)

        for notification in existing_notifications:
            if notification.source_code not in obj["source_codes"]:
                notification.delete(self.db)

        return {"status": "200 - Ok"}

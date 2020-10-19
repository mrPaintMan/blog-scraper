import json
import requests
from flask_restful import Resource
from hyper.contrib import HTTP20Adapter
from server_src.lib.db import Db
from server_src.lib.model import notification_model, register_model, source_model


class Notifications(Resource):

    @classmethod
    def setup(cls, host, resource_path):
        cls.db = Db(host)
        cls.apns_cert = resource_path + "apns.crt.pem"
        cls.apns_key = resource_path + "apns.key.pem"
        return cls

    def get(self):
        notifications = {}
        n_ids = []

        for notification in notification_model.get_all(self.db):
            n_ids.append(notification["n_id"])
            if notification["source_code"] not in notifications:
                notifications[notification["source_code"]] = [notification]

            else:
                notifications[notification["source_code"]].append(notification)

        for source_code, s_notifications in notifications.items():
            source = source_model.get_by_code(self.db, source_code)[0]
            registration = register_model.Registration(None, None, source_code, None)
            registrations = registration.get_by_source_code(self.db)
            self.send_notifications(registrations, s_notifications, source)

        if len(n_ids) > 0:
            notification_model.delete_by_ids(self.db, n_ids)
            
        return {"status": "200 - Ok"}

    def send_notifications(self, registrations, notifications, source):
        base_url = "https://api.sandbox.push.apple.com/3/device/"

        if len(notifications) == 1:
            title = "A new post is available!"
            body = f"{source['name']} has released a new post. Check it out!"
            data = get_payload(title, body, badge=1)

        else:
            title = f"{len(notifications)} new posts are available!"
            body = f"{source['name']} has released new posts. Check them out!"
            data = get_payload(title, body, badge=len(notifications))

        for registration in registrations:
            url = base_url + registration.device_token

            session = requests.Session()
            session.cert = self.apns_cert, self.apns_key
            session.mount(url, HTTP20Adapter())
            session.headers["Content-Type"] = "application/json"
            session.post(url, data=data)


def get_payload(title, body, badge):
    data = {
        'aps':
            {
                'alert':
                    {
                        'title': title,
                        'body': body,
                        'sound': 'default'
                    },
                'badge': badge
            },
        'Simulator Target Bundle': 'com.fpalmqvist.MoBlog'
    }

    return json.dumps(data).encode('utf-8')

import requests


class Notification:
    INSERT_SQL = "INSERT INTO notifications VALUES (DEFAULT, %s, DEFAULT) RETURNING n_id"

    def __init__(self, n_id, post_id):
        self.n_id = n_id
        self.post_id = post_id

    def save(self, db):
        return db.execute(self.INSERT_SQL, self.post_id)[0][0]


def push_notifications(env, host):
    try:
        if env != "prod":
            requests.get(f"http://{host}:5000/blog/notifications")

        else:
            requests.get("https://api.fpalmqvist.com/blog/notifications")

    except Exception as e:
        print("Could not get /notifications. exception:", e)

from datetime import datetime


class Notification:
    SELECT_BY_TOKEN_SQL = "SELECT n_id, device_token, source_code, created FROM notifications WHERE device_token = %s"
    MATCH_SQL = """
                SELECT n_id, device_token, source_code, created 
                FROM notifications 
                WHERE device_token = %s AND source_code = %s
                """
    INSERT_SQL = "INSERT INTO notifications VALUES (DEFAULT, %s, %s, DEFAULT) RETURNING n_id"
    UPDATE_SQL = """
                    UPDATE notifications 
                    SET device_token = %s, source_code = %s, created = %s 
                    WHERE n_id = %s 
                    RETURNING n_id
                 """
    DELETE_ONE_SQL = "DELETE FROM notifications WHERE n_id = %s RETURNING n_id"
    DELETE_ALL_BY_DEVICE_TOKEN_SQL = "DELETE FROM notifications WHERE device_token = %s RETURNING n_id"

    n_id = None
    device_token = None
    source_code = None
    created = None

    def __init__(self, n_id, device_token, source_code, created):
        self.n_id = n_id
        self.device_token = device_token
        self.source_code = source_code
        self.created = created

    def save(self, db):
        if self.n_id is None or self.n_id == 0:
            db.execute(self.INSERT_SQL, (self.device_token, self.source_code))

        else:
            db.execute(self.UPDATE_SQL, (self.device_token, self.source_code, self.created, self.n_id))

    def get_by_device_token(self, db):
        result = []
        data = db.execute(self.SELECT_BY_TOKEN_SQL, self.device_token)

        for notification in data:
            result.append(self.conform_to_notification(notification))

        return result

    def match(self, db):
        data = db.execute(self.MATCH_SQL, (self.device_token, self.source_code))

        if data is not None and len(data) > 0:
            for notification in data:
                self.n_id = notification[0]
                self.created = notification[3]

    def delete(self, db):
        return db.execute(self.DELETE_ONE_SQL, self.n_id)

    def delete_by_device_token(self, db):
        return db.execute(self.DELETE_ALL_BY_DEVICE_TOKEN_SQL, self.device_token)

    def conform_to_notification(self, data):
        time = datetime.timestamp(data[3])
        return Notification(data[0], data[1], data[2], time)

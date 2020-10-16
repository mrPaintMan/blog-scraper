from datetime import datetime


class Registration:
    SELECT_BY_TOKEN_SQL = """
                          SELECT nr_id, device_token, source_code, created 
                          FROM notification_register 
                          WHERE device_token = %s
                          """
    SELECT_BY_SOURCE_CODE_SQL = """
                                SELECT nr_id, device_token, source_code, created 
                                FROM notification_register 
                                WHERE source_code = %s
                                """
    MATCH_SQL = """
                SELECT nr_id, device_token, source_code, created 
                FROM notification_register 
                WHERE device_token = %s AND source_code = %s
                """
    INSERT_SQL = "INSERT INTO notification_register VALUES (DEFAULT, %s, %s, DEFAULT) RETURNING nr_id"
    UPDATE_SQL = """
                 UPDATE notification_register 
                 SET device_token = %s, source_code = %s, created = %s 
                 WHERE nr_id = %s 
                 RETURNING nr_id
                 """
    DELETE_ONE_SQL = "DELETE FROM notification_register WHERE nr_id = %s RETURNING nr_id"
    DELETE_ALL_BY_DEVICE_TOKEN_SQL = "DELETE FROM notification_register WHERE device_token = %s RETURNING nr_id"

    nr_id = None
    device_token = None
    source_code = None
    created = None

    def __init__(self, nr_id, device_token, source_code, created):
        self.nr_id = nr_id
        self.device_token = device_token
        self.source_code = source_code
        self.created = created

    def save(self, db):
        if self.nr_id is None or self.nr_id == 0:
            db.execute(self.INSERT_SQL, (self.device_token, self.source_code))

        else:
            db.execute(self.UPDATE_SQL, (self.device_token, self.source_code, self.created, self.nr_id))

    def get_by_device_token(self, db):
        result = []
        data = db.execute(self.SELECT_BY_TOKEN_SQL, self.device_token)

        for registration in data:
            result.append(self.conform_to_registration(registration))

        return result

    def get_by_source_code(self, db):
        result = []
        data = db.execute(self.SELECT_BY_SOURCE_CODE_SQL, self.source_code)

        for registration in data:
            result.append(self.conform_to_registration(registration))

        return result

    def match(self, db):
        data = db.execute(self.MATCH_SQL, (self.device_token, self.source_code))

        if data is not None and len(data) > 0:
            for registration in data:
                self.nr_id = registration[0]
                self.created = registration[3]

    def delete(self, db):
        return db.execute(self.DELETE_ONE_SQL, self.nr_id)

    def delete_by_device_token(self, db):
        return db.execute(self.DELETE_ALL_BY_DEVICE_TOKEN_SQL, self.device_token)

    def conform_to_registration(self, data):
        time = datetime.timestamp(data[3])
        return Registration(data[0], data[1], data[2], time)



class Source:
    INSERT_SQL = "INSERT INTO source_codes VALUES ('{}', '{}', '{}', '{}', DEFAULT) RETURNING source_code"
    UPDATE_SQL = """
                    UPDATE source_codes 
                    SET description = '{}', profile_image = '{}', alt_image = '{}', created = '{}' 
                    WHERE source_code = '{}'
                    RETURNING source_code
                 """
    SELECT_SQL = """
                    SELECT source_code, description, profile_image, alt_image, created 
                    FROM source_codes 
                    WHERE source_code = '{}'
                 """
    DELETE_SQL = "DELETE FROM source_codes WHERE source_code = '{}' RETURNING source_code"

    def __init__(self, source_code, description, profile_image, alt_image, created):
        self.source_code = source_code
        self.description = description
        self.profile_image = profile_image
        self.alt_image = alt_image
        self.created = created

    def save(self, db):
        data = self.get_by_source_code(db)

        if data is None or len(data) == 0:
            return self.insert(db)

        else:
            self.created = data[0][4]
            return self.update(db)

    def insert(self, db):
        sql = self.INSERT_SQL.format(self.source_code, self.description, self.profile_image, self.alt_image)
        return db.execute(sql)

    def update(self, db):
        sql = self.UPDATE_SQL.format(
            self.description,
            self.profile_image,
            self.alt_image,
            self.created,
            self.source_code,)
        return db.execute(sql)

    def delete(self, db):
        sql = self.DELETE_SQL.format(self.source_code)
        return db.execute(sql)

    def get_by_source_code(self, db):
        sql = self.SELECT_SQL.format(self.source_code)
        return db.execute(sql)

    def match(self, db):
        sql = self.SELECT_SQL.format(self.source_code)
        data = db.execute(sql)
        if data is not None and len(data) == 1:
            self.created = data[0][4]

        elif data is not None and len(data) > 1:
            raise Exception("Multiple rows for source_code: {}".format(self.source_code))

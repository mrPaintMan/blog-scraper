

class Source:
    INSERT_SQL = "INSERT INTO source_codes VALUES (%s, %s, %s, %s, DEFAULT) RETURNING source_code"
    UPDATE_SQL = """
                    UPDATE source_codes 
                    SET description = %s, profile_image = %s, alt_image = %s, created = %s 
                    WHERE source_code = %s
                    RETURNING source_code
                 """
    SELECT_SQL = """
                    SELECT source_code, description, profile_image, alt_image, created 
                    FROM source_codes 
                    WHERE source_code = %s
                 """
    DELETE_SQL = "DELETE FROM source_codes WHERE source_code = %s RETURNING source_code"

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
        return db.execute(self.INSERT_SQL, (self.source_code, self.description, self.profile_image, self.alt_image))

    def update(self, db):
        return db.execute(
            self.UPDATE_SQL,
            (self.description, self.profile_image, self.alt_image, self.created, self.source_code))

    def delete(self, db):
        return db.execute(self.DELETE_SQL, self.source_code)

    def get_by_source_code(self, db):
        return db.execute(self.SELECT_SQL, self.source_code)

    def match(self, db):
        data = db.execute(self.SELECT_SQL, self.source_code)
        if data is not None and len(data) == 1:
            self.created = data[0][4]

        elif data is not None and len(data) > 1:
            raise Exception(f"Multiple rows for source_code: {self.source_code}")

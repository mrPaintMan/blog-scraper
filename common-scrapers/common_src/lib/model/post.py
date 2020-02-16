

class Post:
    INSERT_SQL = "INSERT INTO posts VALUES (DEFAULT, '{}', '{}', '{}', '{}', DEFAULT) RETURNING post_id"
    UPDATE_SQL = """
                    UPDATE posts 
                    SET post_id = {}, ext_id = '{}', title = '{}', link = '{}', source_code = '{}', created = '{}' 
                    WHERE post_id = {}
                    RETURNING post_id
                 """
    SELECT_SQL = """
                    SELECT post_id, ext_id, title, link, source_code, created 
                    FROM posts 
                    WHERE ext_id = '{}' AND source_code = '{}'
                 """
    DELETE_SQL = "DELETE FROM posts WHERE post_id = {} RETURNING post_id"

    def __init__(self, post_id, ext_id, title, link, source_code, created):
        self.post_id = post_id
        self.ext_id = ext_id
        self.title = title.replace("'", "''")
        self.link = link.replace("'", "''")
        self.source_code = source_code
        self.created = created

    def save(self, db):
        if self.post_id is None or self.post_id == 0:
            return self.insert(db)

        else:
            return self.update(db)

    def insert(self, db):
        sql = self.INSERT_SQL.format(self.ext_id, self.title, self.link, self.source_code)
        return db.execute(sql)

    def update(self, db):
        sql = self.UPDATE_SQL.format(
            self.post_id,
            self.ext_id,
            self.title,
            self.link,
            self.source_code,
            self.created,
            self.post_id,)
        return db.execute(sql)

    def delete(self, db):
        sql = self.DELETE_SQL.format(self.post_id)
        return db.execute(sql)

    def get_by_ext_id_and_source(self, db):
        sql = self.SELECT_SQL.format(self.ext_id, self.source_code)
        return db.execute(sql)

    def match(self, db):
        sql = self.SELECT_SQL.format(self.ext_id, self.source_code)
        data = db.execute(sql)
        if data is not None and len(data) == 1:
            self.post_id = data[0][0]
            self.created = data[0][5]

        elif data is not None and len(data) > 1:
            raise Exception("Multiple rows for ext_id: {} and source_code {}".format(self.ext_id, self.source_code))



class Post:
    INSERT_SQL = "INSERT INTO posts VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, DEFAULT) RETURNING post_id"
    UPDATE_SQL = """
                    UPDATE posts 
                    SET ext_id = %s, 
                        title = %s, 
                        link = %s, 
                        image = %s, 
                        alt_image = %s, 
                        source_code = %s, 
                        created = %s 
                    WHERE post_id = %s
                    RETURNING post_id
                 """
    SELECT_SQL = """
                    SELECT post_id, ext_id, title, link, image, alt_image, source_code, created 
                    FROM posts 
                    WHERE link = %s AND source_code = %s
                 """
    DELETE_SQL = "DELETE FROM posts WHERE post_id = %s RETURNING post_id"

    def __init__(self, post_id, ext_id, title, link, image, alt_image, source_code, created):
        self.post_id = post_id
        self.ext_id = ext_id
        self.title = title.replace("'", "''")
        self.link = link.replace("'", "''")
        self.image = image
        self.alt_image = alt_image
        self.source_code = source_code
        self.created = created

    def save(self, db):
        if self.post_id is None or self.post_id == 0:
            return self.insert(db)

        else:
            return self.update(db)

    def insert(self, db):
        return db.execute(
            self.INSERT_SQL,
            (self.ext_id, self.title, self.link, self.image, self.alt_image, self.source_code))[0][0]

    def update(self, db):
        return db.execute(
            self.UPDATE_SQL,
            (
                self.ext_id,
                self.title,
                self.link,
                self.image,
                self.alt_image,
                self.source_code,
                self.created,
                self.post_id
            )
        )[0][0]

    def delete(self, db):
        return db.execute(self.DELETE_SQL, self.post_id)[0][0]

    def match(self, db):
        data = db.execute(self.SELECT_SQL, (self.link, self.source_code))
        if data is not None and len(data) == 1:
            self.post_id = data[0][0]
            self.created = data[0][7]

        elif data is not None and len(data) > 1:
            raise Exception(f"Multiple rows for link: {self.link} and source_code {self.source_code}")

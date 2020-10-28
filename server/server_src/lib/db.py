import pg8000


class Db:
    def __init__(self, host):
        self.conn = pg8000.connect(
            database="blogscraper",
            user="app",
            password="vh38pt94dx",
            host=host,
            port=5432
        )
        self.conn.autocommit = True

        self.cur = self.conn.cursor()

    def execute(self, sql, values=None):
        data = None

        if values is not None and type(values) != tuple:
            # To ensure values always is a tuple
            values = (values,)

        try:
            if values is not None:
                self.cur.execute(sql, values)
            else:
                self.cur.execute(sql)

            data = self.cur.fetchall()

        except pg8000.Error as e:
            print("something went wrong:", e, sql)
            self.rollback()

        return data

    def commit(self):
        if self.conn:
            self.conn.commit()

    def rollback(self):
        if self.conn:
            self.conn.rollback()

    def close(self):
        if self.conn:
            self.conn.close()

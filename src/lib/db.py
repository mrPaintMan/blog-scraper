import pg8000


class Db:
    DEFAULT_CONN_STR = "filippalmqvist;filippalmqvist;/tmp/.s.PGSQL.5432"

    def __init__(self, conn_string):
        conn_strings = conn_string.split(';')
        self.conn = pg8000.connect(
            user=conn_strings[0],
            password=conn_strings[1],
            database="blogscraper",
            host="localhost",
            port=5432
        )

        self.cur = self.conn.cursor()

    def execute(self, sql):
        data = None
        try:
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

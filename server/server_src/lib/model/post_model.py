from datetime import datetime

SELECT_ONE_SQL = """
                    SELECT post_id, ext_id, title, link, source_code, created 
                    FROM posts 
                    WHERE post_id = {}
                 """
SELECT_ALL_PAG_SQL = """
                        SELECT * FROM (
                            SELECT *, ROW_NUMBER() OVER(ORDER BY post_id DESC)
                            FROM posts
                        ) as x
                        WHERE row_number > {} * 10
                        LIMIT 10
                    """
SELECT_SOURCE_PAG_SQL = """
                            SELECT * FROM (
                                SELECT *, ROW_NUMBER() OVER(ORDER BY post_id DESC)
                                FROM posts
                                WHERE source_code = '{}'
                            ) as x
                            WHERE row_number > {} * 10
                            LIMIT 10
                        """


def get_by_id(db, post_id):
    sql = SELECT_ONE_SQL.format(post_id)
    data = db.execute(sql)
    result = []

    for post in data:
        result.append(conform_to_post(post))

    return result


def get_pag(db, pagination):
    sql = SELECT_ALL_PAG_SQL.format(pagination)
    data = db.execute(sql)
    result = []

    for post in data:
        result.append(conform_to_post(post))

    return result


def get_pag_by_source(db, pagination, sourcecode):
    sql = SELECT_SOURCE_PAG_SQL.format(sourcecode, pagination)
    data = db.execute(sql)
    result = []

    for post in data:
        result.append(conform_to_post(post))

    return result


def conform_to_post(data):

    time = datetime.timestamp(data[5])
    return {
        "post_id": data[0],
        "ext_id": data[1],
        "title": data[2],
        "link": data[3],
        "source_code": data[4],
        "created": time
    }

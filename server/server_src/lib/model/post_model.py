from datetime import datetime

SELECT_ONE_SQL = """
                    SELECT post_id, ext_id, title, link, image, alt_image, source_code, created 
                    FROM posts 
                    WHERE post_id = %s
                 """
SELECT_ALL_PAG_SQL = """
                        SELECT * FROM (
                            SELECT *, ROW_NUMBER() OVER(ORDER BY ext_id DESC)
                            FROM posts
                        ) as x
                        WHERE row_number > %s * 10
                        LIMIT 10
                    """
SELECT_SOURCE_PAG_SQL = """
                            SELECT * FROM (
                                SELECT *, ROW_NUMBER() OVER(ORDER BY ext_id DESC)
                                FROM posts
                                WHERE source_code = %s
                            ) as x
                            WHERE row_number > %s * 10
                            LIMIT 10
                        """


def get_by_id(db, post_id):
    data = db.execute(SELECT_ONE_SQL, post_id)
    result = []

    for post in data:
        result.append(conform_to_post(post))

    return result


def get_pag(db, pagination):
    data = db.execute(SELECT_ALL_PAG_SQL, pagination)
    result = []

    for post in data:
        result.append(conform_to_post(post))

    return result


def get_pag_by_source(db, pagination, sourcecode):
    data = db.execute(SELECT_SOURCE_PAG_SQL, (sourcecode, pagination))
    result = []

    for post in data:
        result.append(conform_to_post(post))

    return result


def conform_to_post(data):
    time = datetime.timestamp(data[7])
    return {
        "post_id": data[0],
        "ext_id": data[1],
        "title": data[2],
        "link": data[3],
        "image": data[4],
        "alt_image": data[5],
        "source_code": data[6],
        "created": time
    }

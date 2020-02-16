from datetime import datetime

SELECT_ONE_SQL = """
                    SELECT source_code, description, created
                    FROM source_codes 
                    WHERE source_code = '{}'
                 """
SELECT_ALL_SQL = """
                    SELECT source_code, description, created
                    FROM source_codes
                 """


def get_by_code(db, source_code):
    sql = SELECT_ONE_SQL.format(source_code)
    data = db.execute(sql)
    result = []

    for source in data:
        result.append(conform_to_source(source))

    return result


def get_all(db):
    sql = SELECT_ALL_SQL
    data = db.execute(sql)
    result = []

    for source in data:
        result.append(conform_to_source(source))

    return result


def conform_to_source(data):

    time = datetime.timestamp(data[2])
    return {
        "source_code": data[0],
        "description": data[1],
        "created": time
    }
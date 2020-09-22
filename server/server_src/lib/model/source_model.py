from datetime import datetime

SELECT_ONE_SQL = """
                    SELECT source_code, description, profile_image, alt_image, created
                    FROM source_codes 
                    WHERE source_code = %s
                 """
SELECT_ALL_SQL = """
                    SELECT source_code, description, profile_image, alt_image, created
                    FROM source_codes
                 """


def get_by_code(db, source_code):
    data = db.execute(SELECT_ONE_SQL, source_code)
    result = []

    for source in data:
        result.append(conform_to_source(source))

    return result


def get_all(db):
    data = db.execute(SELECT_ALL_SQL)
    result = []

    for source in data:
        result.append(conform_to_source(source))

    return result


def conform_to_source(data):
    time = datetime.timestamp(data[4])
    return {
        "source_code": data[0],
        "description": data[1],
        "profile_image": data[2],
        "alt_image": data[3],
        "created": time
    }

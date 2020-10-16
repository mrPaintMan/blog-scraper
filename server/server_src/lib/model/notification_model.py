from datetime import datetime

SELECT_ALL_SQL = """
                 SELECT n_id, notifications.post_id, source_code, notifications.created 
                 FROM notifications
                 JOIN posts ON notifications.post_id = posts.post_id
                 """
DELETE_BY_IDS = "DELETE FROM notifications WHERE n_id = ANY(%s) RETURNING n_id"


def get_all(db):
    data = db.execute(SELECT_ALL_SQL)
    result = []

    for notification in data:
        result.append(conform_to_notification(notification))

    return result


def delete_by_ids(db, ids):
    return db.execute(DELETE_BY_IDS, (ids,))


def conform_to_notification(data):
    time = datetime.timestamp(data[3])
    return {
        "n_id": data[0],
        "post_id": data[1],
        "source_code": data[2],
        "created": time
    }

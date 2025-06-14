from models.db import db


def fill_db(data, db_class):
    db.drop_all()
    db.create_all()

    for item in data:
        db.session.add(db_class(**item))

    db.session.commit()

import shelve

def set_value(path, key, value):
    with shelve.open(path) as db:
        db[key] = value

def get_value(path, key, default=None):
    with shelve.open(path) as db:
        return db.get(key, default)

def get_all(path):
        with shelve.open(path) as db:
            return dict(db)

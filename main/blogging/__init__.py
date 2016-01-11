from main import app, db
from main.security import User

from flask.ext.blogging import SQLAStorage, BloggingEngine


storage = SQLAStorage(db=db)
blogging_engine = BloggingEngine(app, storage)


@blogging_engine.user_loader
def load_user(userid):
#    print("tables:", db.tables.keys())
    return User(userid)


def configure_blogging():
    db.create_all(bind=['blog'])

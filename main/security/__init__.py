from main import app, db

from flask.ext.security import Security, SQLAlchemyUserDatastore, \
        UserMixin, RoleMixin, login_required, utils

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
        schema = 'security'
        )

#class RoleUsers(db.Model):
#    __bind_key__ = 'security'
#    __tablename__ = 'roles_users'
#    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
#    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __bind_key__ = 'security'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __bind_key__ = 'security'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', 
            secondary=roles_users, 
            backref=db.backref('users',lazy='dynamic'))


    # Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


def configure_security():
    # Create any database tables that don't exist yet.
    db.create_all()

    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='end-user', description='End user')


    # Create two Users for testing purposes -- unless they already exists.
    # In each case, use Flask-Security utility function to encrypt the password.
    encrypted_password = utils.encrypt_password('password')
    if not user_datastore.get_user('someone@example.com'):
        user_datastore.create_user(email='someone@example.com', password=encrypted_password)
    if not user_datastore.get_user('admin@example.com'):
        user_datastore.create_user(email='admin@example.com',
                password=encrypted_password)

    db.session.commit()

    # Give one User has the "end-user" role, while the other has the "admin" role. 
    #(This will have no effect if the
    # Users already have these Roles.) Again, commit any database changes.
    user_datastore.add_role_to_user('someone@example.com', 'end-user')
    user_datastore.add_role_to_user('admin@example.com', 'admin')

    db.session.commit()




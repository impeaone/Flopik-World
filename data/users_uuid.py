import sqlalchemy
from data import db_session
from werkzeug.security import generate_password_hash, check_password_hash


class User_uuid(db_session.SqlAlchemyBase):
    __tablename__ = 'users_uuid'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    uuid = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

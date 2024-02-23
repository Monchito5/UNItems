from werkzeug.security import check_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, email, password, username="", auth="", imgprofile="") -> None:
        self.id = id
        self.password = password
        self.email = email
        self.username= username
        self.auth = auth
        self.imgprofile = imgprofile
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
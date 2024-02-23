from .entities.User import User


class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, password, username, auth, imgprofile FROM user 
                    WHERE email = '{}'""".format(user.email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], user.email, User.check_password(row[1], user.password), username=row[2], auth=row[3], imgprofile=row[4])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT email, password, username, auth, imgprofile FROM user WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(id, row[0], row[1], username=row[2], auth=row[3], imgprofile=row[4])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
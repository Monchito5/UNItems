from .entities.User import User


class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, password, username, fullname, age, schoolgrade, auth, imgprofile FROM user 
                    WHERE email = '{}'""".format(user.email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], user.email, User.check_password(row[1], user.password), username=row[2], fullname=row[3], age=row[4], schoolgrade=row[5], auth=row[6], imgprofile=row[7])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT email, password, username, fullname, age, schoolgrade, auth, imgprofile FROM user WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(id, row[0], row[1], username=row[2], fullname=row[3], age=row[4], schoolgrade=row[5], auth=row[6], imgprofile=row[7])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
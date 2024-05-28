from .entities.Feeds import Feeds


class ModelFeed():
    @classmethod
    def get_by_id(self, db, feed_id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT feed_id, datepublicate, title, content, imgcontent, feedcomments FROM feeds WHERE feed_id = {}".format(feed_id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Feeds(feed_id, row[0], row[1], title=row[2], content=row[3], imgcontent=row[4], feedcomments=row[5])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
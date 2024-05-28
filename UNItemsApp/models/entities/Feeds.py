
class Feeds():

    def __init__(self, feed_id, datepublicate, title="", content="", imgcontent="", feedcomments="", author_id="current_user") -> None:
        self.feed_id = feed_id
        self.datepublicate = datepublicate
        self.title = title
        self.content = content
        self.imgcontent = imgcontent
        self.feedcomments = feedcomments
        self.author_id = author_id
class config:
    SECRET_KEY = 'unitems5'

class DevelompentConfig(config):
    DEBUG = True
    MYSQL_HOST      = 'localhost'
    MYSQL_USER      = 'root'
    MYSQL_PASSWORD  = ''
    MYSQL_DB        = 'unitemsapp'

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = "***************"
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    MAIL_PASSWORD = "**************"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

config = {'development' : DevelompentConfig}
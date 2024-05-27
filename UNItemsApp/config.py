import ssl
class config:
    # False Secret no se espante compa
    secret = 'dakgk395ujkfmdkji4jijo3jigfmkgdmwñm' 
    SECRET_KEY = 'secret'
    
class DevelompentConfig(config):
    DEBUG = True
    MYSQL_HOST      = 'localhost'
    MYSQL_USER      = 'root'
    MYSQL_PASSWORD  = ''
    MYSQL_DB        = 'unitems'

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = "@gmail.com"
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    MAIL_PASSWORD = "secret"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    context = ssl.create_default_context()
    context.set_ciphers('DEFAULT@SECLEVEL=1')
    MAIL_SSL_CONTEXT = context

config = {'development' : DevelompentConfig}
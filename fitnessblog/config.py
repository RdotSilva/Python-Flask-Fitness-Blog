from config_secret import SECRET, SQLALCHEMY_DATABASE_URI, MAIL_USER, MAIL_PASS


class Config:
    # Config variables imported from config_secret.py
    SECRET_KEY = SECRET
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI

    # Mail config settings
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = MAIL_USER
    MAIL_PASSWORD = MAIL_PASS

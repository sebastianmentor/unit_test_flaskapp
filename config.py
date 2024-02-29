from dotenv import load_dotenv
import os

load_dotenv()

class SecurityConfig:
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    SECRET_KEY = os.getenv('SECRET_KEY')

class MailConfig(SecurityConfig):
    MAIL_SERVER = '127.0.0.1'
    MAIL_PORT = 1025
    MAIL_USE_SSL = False
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'email@example.com'     
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = '"MyApp" <noreply@example.com>'
    SECURITY_EMAIL_SENDER = '"MyApp" <noreply@example.com>'
    SECURITY_CONFIRMABLE = True
    SECURITY_REGISTERABLE = False

class ConfigDebug(MailConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_LOCAL')

    DEBUG=True
    TESTING=False

class ConfigProduction(MailConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_LOCAL')

    DEBUG=False
    TESTING=False

    USER_ENABLE_CHANGE_PASSWORD = False
    USER_ENABLE_REGISTER = False

class ConfigTest(MailConfig):
    SERVER_NAME = "BankApp.com"
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_LOCAL')


    TESTING = True
    DEBUG=False
class GeneralConfig(object):
    APP_NAME = 'CrestPoint'
    SECRET_KEY='notsecured'
    
class DevelopmentConfig(GeneralConfig):
    SECRET_KEY='qwertyujbvcxfdzfghshfdahsdjgheqigfhiqegkqegfeqfqejuovbqaquyifv'
    SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root@localhost/crestpointdb'
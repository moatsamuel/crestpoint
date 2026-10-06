from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from pkg import config
from pkg.main.routes import main
from pkg.admin.routes import admin
from pkg.patients.routes import patients
from pkg.doctor.routes import doctors

load_dotenv()

csrf = CSRFProtect()

def create_app():
    from pkg.models import db
    app = Flask(__name__)
    # app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config.from_object(config.DevelopmentConfig)
    
    app.register_blueprint(main)
    app.register_blueprint(admin,url_prefix='/admin')
    app.register_blueprint(patients,url_prefix='/patients')
    app.register_blueprint(doctors,url_prefix='/doctor')

    db.init_app(app)
    
    migrate = Migrate(app,db)
    csrf.init_app(app)
    
    return app
    
app = create_app()



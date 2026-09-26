from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from pkg import config

load_dotenv()

# csrf = CSRFProtect()

def create_app():
    from pkg.models import db
    app = Flask(__name__)
    # app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config.from_object(config.DevelopmentConfig)

    db.init_app(app)
    
    migrate = Migrate(app,db)
    # csrf.init_app(app)
    
    return app
    
app = create_app()

from pkg import routes



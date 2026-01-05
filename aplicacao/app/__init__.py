from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    #Configurações
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
    app.config['SECRET_KEY'] = 'teste' #Mudar Depois,
    from datetime import timedelta
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    db.init_app(app)
    #Blueprints
    from app.routes.home import home_bp
    app.register_blueprint(home_bp)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    
    
    
    with app.app_context():
        db.create_all() #Para produção é ideal usar migração
    return app

    
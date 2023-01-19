from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "d0a9586ec1d02d6db97b6709d0e319d38400acab8ebe7d91f1617efb736a33c7" #คอม wachiss35
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    login_manager_ggauth = LoginManager()
    login_manager_ggauth.login_view = 'auth.callback'
    login_manager_ggauth.init_app(app)

    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @login_manager_ggauth.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    with app.app_context():
        db.create_all()

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # blueprint for on-click parts of app
    from .onclick import onclick as onclick_blueprint
    app.register_blueprint(onclick_blueprint)
    return app

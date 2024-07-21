import os
from dotenv import load_dotenv
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user


db = SQLAlchemy()

from board import (
    database,
    errors,
    pages,
    auth,
    student,
)
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    app.logger.setLevel("INFO")

    database.init_app(app)

    app.register_blueprint(pages.bp)
    app.register_blueprint(student.bp)
    app.register_blueprint(auth.auth)
    app.register_error_handler(404, errors.page_not_found)
    app.logger.debug(f"Current Environment: {os.getenv('ENVIRONMENT')}")
    app.logger.debug(f"Using Database: {app.config.get('DATABASE')}")
    #app.logger.debug(f"Using SQLALCHEMY_DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    
    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    
    # Middleware to track previous URL
    @app.before_request
    def track_previous_url():
        if 'previous_url' in session:
            session['previous_url'] = request.url
        else:
            session['previous_url'] = request.url
    
    # Context processor to inject current route and referrer
    @app.context_processor
    def inject_current_route():
        return dict(current_route=request.endpoint, previous_url=request.referrer, is_authenticated=current_user.is_authenticated)

    
    return app
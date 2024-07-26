import os
from dotenv import load_dotenv
from flask import Flask, request, session, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

# Load environment variables
load_dotenv()

# Initialize the SQLAlchemy database instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    app.logger.setLevel("INFO")

    # Set the SQLALCHEMY database URI from the environment variable
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('FLASK_SQLALCHEMY_DATABASE_URI')

    # Optionally log the database URI for debugging
    app.logger.debug(f"Using Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Initialize the database with the app
    db.init_app(app)

    # Import the database module here to avoid circular imports
    from . import database
    database.init_app(app)

    # Create the upload directory
    with app.app_context():
        os.makedirs(os.path.join(current_app.instance_path, 'pdfs'), exist_ok=True)

    # Register blueprints
    from . import errors, pages, auth, student, teacher
    app.register_blueprint(pages.bp)
    app.register_blueprint(student.bp)
    app.register_blueprint(auth.auth)
    app.register_blueprint(teacher.bp)
    app.register_error_handler(404, errors.page_not_found)

    # Initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Import models here to avoid circular imports
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
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

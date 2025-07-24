# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_mail import Mail
# from config import Config
#
# db = SQLAlchemy()
# mail = Mail()

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)
#
#     db.init_app(app)
#     mail.init_app(app)
#
#     from python_webapp.routes.main import bp as main_bp
#     app.register_blueprint(main_bp)
#
#     return app

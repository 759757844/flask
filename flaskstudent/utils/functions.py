import os


from flask import Flask

from views.user import user
from views.student import student
from views.grade import grade
from views.permission import permission
from views.role import role
from App.models import db


def create_app():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)

    app.register_blueprint(blueprint=user, url_prefix='/user')
    app.register_blueprint(blueprint=student, url_prefix='/student')
    app.register_blueprint(blueprint=grade, url_prefix='/grade')
    app.register_blueprint(blueprint=permission, url_prefix='/permission')
    app.register_blueprint(blueprint=role, url_prefix='/role')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@127.0.0.1:3306/flaskmanagement'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 设置session密钥
    app.config['SECRET_KEY'] = 'secret_key'

    db.init_app(app=app)

    with app.app_context():
        db.create_all()

    return app

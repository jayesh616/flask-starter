from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_admin import Admin
from marshmallow import ValidationError
from celery import Celery
from flask_login import LoginManager

from db import db
from ma import ma
from resources.v1.user import UserRegister, UserLogin, User, UserLogout, TokenRefresh
from models.user import UserModel
from models.account import AccountModel

from admin.auth import auth as auth_blueprint


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"]
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app = Flask(__name__)
app.config.from_envvar("APPLICATION_SETTINGS")
api = Api(app)
jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)
celery = make_celery(app)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


# Shell Commands Start
@app.shell_context_processor
def inject_models():
    return {
        'UserModel': UserModel,
        'AccountModel': AccountModel
    }
# Shell Commands End


# API V1 Start
api_v1 = "/api/v1"
api.add_resource(UserRegister, api_v1+"/register")
api.add_resource(User, api_v1+"/user/<int:user_id>")
api.add_resource(UserLogin, api_v1+"/login")
api.add_resource(UserLogout, api_v1+"/logout")
api.add_resource(TokenRefresh, api_v1+"/refresh")
# API V1 End

if __name__ == "__main__":
    ma.init_app(app)

    from admin.views import MyAdminIndexView, LogoutMenuLink
    from admin.user import UserModelView

    # Admin View Start
    admin = Admin(app, name="Admin", template_mode="bootstrap3", index_view=MyAdminIndexView())
    admin.add_view(UserModelView(UserModel, db.session, "User"))
    admin.add_link(LogoutMenuLink(name="Logout", category='', url="/logout"))
    # Admin View End

    login_manager = LoginManager()
    login_manager.login_view = "admin.auth.login"
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        return AccountModel.query.get(int(user_id))

    # from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    app.run(port=5001, debug=True, host="0.0.0.0")

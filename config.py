import os


DEBUG=False
PAGE_SIZE=20
SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URI")
FLASK_ADMIN_SWATCH="cerulean"
SENDGRID_API_KEY=os.environ.get("SENDGRID_API_KEY")
SENDGRID_DEFAULT_FROM=os.environ.get("SENDGRID_DEFAULT_FROM")
SECRET_KEY=os.environ.get("SECRET_KEY")
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = [
    "access",
    "refresh",
]
CELERY_BROKER_URL=os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND=os.environ.get("CELERY_RESULT_BACKEND")

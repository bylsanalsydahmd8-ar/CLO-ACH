from flask import Flask, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, CSRFError

# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# CREATE FLASK APP
# =========================================================

app = Flask(__name__)


# =========================================================
# SECRET KEY
# =========================================================

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is missing from your .env file."
    )

app.config["SECRET_KEY"] = SECRET_KEY


# =========================================================
# DATABASE
# =========================================================

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

if not all([
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_NAME
]):
    raise RuntimeError(
        "Database environment variables are missing. "
        "Check DB_USER, DB_PASSWORD, DB_HOST and DB_NAME."
    )


app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{DB_USER}:"
    f"{DB_PASSWORD}@"
    f"{DB_HOST}/"
    f"{DB_NAME}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

db = SQLAlchemy(app)


# =========================================================
# MIGRATION
# =========================================================

migrate = Migrate(app, db)


# =========================================================
# CSRF PROTECTION
# =========================================================

csrf = CSRFProtect(app)

# Optional:
# CSRF tokens are valid for 1 hour.
app.config["WTF_CSRF_TIME_LIMIT"] = 3600


# =========================================================
# FLASK LOGIN
# =========================================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

login_manager.login_message = (
    "Please login to access this page."
)

login_manager.login_message_category = "warning"


# =========================================================
# USER LOADER
# =========================================================

@login_manager.user_loader
def load_user(user_id):

    from student.models import User

    return User.query.get(int(user_id))


# =========================================================
# CSRF ERROR HANDLER
# =========================================================

@app.errorhandler(CSRFError)
def handle_csrf_error(error):

    print("")
    print("=" * 60)
    print("❌ CSRF ERROR")
    print("=" * 60)
    print("Reason:", error.description)
    print("Request:", request.method, request.path)
    print("Form:", request.form)
    print("=" * 60)
    print("")

    flash(
        f"CSRF Error: {error.description}",
        "danger"
    )

    return redirect(
        request.referrer
        or url_for("question_clo_matrix")
    )


# =========================================================
# IMPORT ROUTES LAST
# =========================================================

from student import routes
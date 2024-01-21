from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/')
main_bp = Blueprint('main', __name__, url_prefix='/')

from . import auth, main 

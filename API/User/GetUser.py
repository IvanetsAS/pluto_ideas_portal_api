import json

from flask import Blueprint, render_template
from flask import current_app as app
from Classes.BaseResponse import BaseResponse

# Blueprint Configuration
user_getuser_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@user_getuser_bp.route('/user/get_user', methods=['GET'])
def GetUser():
    """/user/get_user"""
    return BaseResponse(True, app.current_user).serialize()
# -*- coding: utf-8 -*-

import flask
from flask import current_app as app, request
from pluto_ideas_api.Classes.BaseResponse import BaseResponse

# Blueprint Configuration
user_getuser_bp = flask.Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@user_getuser_bp.route('/user/get_user', methods=['GET'])
def GetUser():
    """/user/get_user"""
    id = request.args.get('id')
    print(id)
    return BaseResponse(True, app.current_user).serialize()
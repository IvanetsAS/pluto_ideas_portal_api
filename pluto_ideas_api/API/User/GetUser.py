# -*- coding: utf-8 -*-
import json

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
    return json.dumps({'result': True, 'data': app.current_user})


@user_getuser_bp.after_request
def add_cors_headers(response):
    r = request.referrer[:-1]
    white = ['http://localhost:3000', 'http://localhost:8080']

    if r in white:
        response.headers.add('Access-Control-Allow-Origin', r)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
        response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
        response.headers.add('Access-Control-Allow-Headers', 'Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    return response

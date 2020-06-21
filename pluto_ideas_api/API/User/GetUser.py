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
    # id = request.args.get('id')
    # print(id)
    current_user = app.current_user.copy()
    user_achievements = [achievement for achievement in app.achievements if achievement["id"] in current_user["achievements"]]

    current_user.pop("achievements")
    current_user.update({"achievements":user_achievements})

    current_user_ideas = []

    for idea_group in app.ideas:
        for idea in idea_group['ideas']:
            if idea['author_id'] == current_user['user_id']:
                current_user_ideas.append(idea)

    current_user_ideas.sort(key=lambda n: n["rating"], reverse=True)
    current_user.update({"ideas":current_user_ideas})


    return '{"result": true, "data": ' + str(current_user).replace("\'", "\"") + '}'
    # return json.dumps({'result': True, 'data': app.current_user})


@user_getuser_bp.after_request
def add_cors_headers(response):
    if request.referrer is not None:
        r = request.referrer[:-1]
        white = ['http://localhost:3000', 'http://localhost:8080', 'http://45.90.34.42']

        if r in white:
            response.headers.add('Access-Control-Allow-Origin', r)
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
            response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
            response.headers.add('Access-Control-Allow-Headers', 'Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    return response

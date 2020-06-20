# -*- coding: utf-8 -*-
import json

import flask
from flask import current_app as app, request

from pluto_ideas_api.Classes.BaseResponse import BaseResponse

# Blueprint Configuration
idea_getgroupbytag_bp = flask.Blueprint(
    'getgroupbytag', __name__,
    template_folder='templates',
    static_folder='static'
)


@idea_getgroupbytag_bp.route('/idea/get_group_by_tag', methods=['POST'])
def get_group_by_tag():
    """/idea/get_group_by_tag"""
    # tag = request.args.get('tag').lower().replace("\'", "").replace('\"', "")
    tag_json = request.json

    if "tag" in tag_json:
        tag = tag_json["tag"].lower()

        for idea_group in app.ideas:
            for idea in idea_group['ideas']:
                if tag.lower() in idea['tags']:
                    return '{"result": true, "data": ' + str(idea_group).replace("\'", "\"") + '}'

    return '{"result": false, "data": []}'


@idea_getgroupbytag_bp.after_request
def add_cors_headers(response):
    if request.referrer is not None:

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


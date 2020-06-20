# -*- coding: utf-8 -*-
import json

import flask
from flask import current_app as app, request


# Blueprint Configuration
tag_gettagsrating_bp = flask.Blueprint(
    'gettagsrating_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@tag_gettagsrating_bp.route('/tag/get_tags_rating', methods=['GET'])
def get_tags_rating():
    """/tag/get_tags_rating"""
    data = app.ideas
    ideas = []
    for group in data:
        ideas += group['ideas']

    tag_dict = {}
    for idea in ideas:
        for tag in idea['tags']:
            if tag in tag_dict:
                tag_dict[tag] += 1
            else:
                tag_dict[tag] = 1
    tags = list(tag_dict.items())
    tags.sort(key=lambda x: x[1], reverse=True)

    return json.dumps({'result': True, 'tags': [{'name': tag, 'rating': count} for tag, count in tags]})

@tag_gettagsrating_bp.after_request
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
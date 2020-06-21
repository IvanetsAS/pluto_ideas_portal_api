# -*- coding: utf-8 -*-
import json

import flask
from flask import current_app as app, request

from pluto_ideas_api.Classes.BaseResponse import BaseResponse

# Blueprint Configuration
idea_addideatogroup_bp = flask.Blueprint(
    'addideatogroup', __name__,
    template_folder='templates',
    static_folder='static'
)


@idea_addideatogroup_bp.route('/idea/add_idea_to_group', methods=['POST'])
def add_idea_to_group():
    """/idea/add_idea_to_group"""
    text_json = request.json
    group_id = text_json['group_id']
    text = text_json['text']
    tags = text_json['tags']
    name = text_json['name']
    author_id = text_json['author_id']
    for group in app.ideas:
        if group['id'] == group_id:
            max_id = 0
            for idea in group['ideas']:
                if idea['id'] > max_id:
                    max_id = idea['id']
            group['ideas'].append({
                'id': max_id + 1,
                'name': name,
                'rating': 1,
                'text': text,
                'tags': tags,
                'author_id': author_id
            })
    return '{"result": true}'


@idea_addideatogroup_bp.after_request
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

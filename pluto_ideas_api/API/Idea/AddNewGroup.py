# -*- coding: utf-8 -*-
import json

import flask
from flask import current_app as app, request

from pluto_ideas_api.Classes.BaseResponse import BaseResponse

# Blueprint Configuration
idea_addnewgroup_bp = flask.Blueprint(
    'addnewgroup', __name__,
    template_folder='templates',
    static_folder='static'
)


@idea_addnewgroup_bp.route('/idea/add_new_group', methods=['POST'])
def add_new_group():
    """/idea/add_new_group"""
    text_json = request.json
    text = text_json['text']
    tags = text_json['tags']
    name = text_json['name']
    group_name = text_json['group_name']
    author_id = text_json['author_id']
    max_id = 0
    for group in app.ideas:
        if group['id'] > max_id:
            max_id = group['id']
    app.ideas.append({
        "id": max_id + 1,
        "name": group_name,
        "ideas": [
            {
                "name": name,
                "id": 1,
                "author_id": author_id,
                "text": text,
                "tags": tags,
                "rating": 1
            }
        ],

    })
    return '{"result": true}'

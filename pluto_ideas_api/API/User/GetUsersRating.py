# -*- coding: utf-8 -*-
import json

import flask
from flask import current_app as app, request

# Blueprint Configuration
tag_getusersrating_bp = flask.Blueprint(
    'getusersrating_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@tag_getusersrating_bp.route('/user/get_users_rating', methods=['GET'])
def get_group_by_tag():
    """/user/get_users_rating"""
    data = app.ideas
    ideas = []
    for group in data:
        ideas += group['ideas']

    user_dict = {}
    for idea in ideas:
        if idea['author_id'] in user_dict:
            user_dict[idea['author_id']] += 1
        else:
            user_dict[idea['author_id']] = 1
    users = list(user_dict.items())
    users.sort(key=lambda x: x[1], reverse=True)

    return json.dumps(
        {'result': True, 'users': [{'name': 'Александр', 'id': tag, 'rating': count} for tag, count in users]})

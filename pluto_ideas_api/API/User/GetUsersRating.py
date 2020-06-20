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


def get_user_name(user_id, users):
    for user in users:
        if user['user_id'] == user_id:
            return user['first_name']


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

    return json.dumps({'result': True,
                       'users': [{'name': get_user_name(tag, app.users), 'id': tag, 'rating': count}
                                 for tag, count in users]
                       })

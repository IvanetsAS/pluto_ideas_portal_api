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


@tag_gettagsrating_bp.route('/tag/get_tag_rating', methods=['GET'])
def get_group_by_tag():
    """/tag/get_tag_rating"""
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

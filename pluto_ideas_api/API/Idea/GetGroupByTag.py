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

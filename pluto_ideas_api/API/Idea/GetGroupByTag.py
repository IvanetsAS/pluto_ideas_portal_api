# -*- coding: utf-8 -*-

import flask
from flask import current_app as app, request

from pluto_ideas_api.Classes.BaseResponse import BaseResponse
from pluto_ideas_api.Classes.textprocess.most_relevant_bm25_lematized import get_relevance_list

# Blueprint Configuration
idea_getgroupbytag_bp = flask.Blueprint(
    'getgroupbytag', __name__,
    template_folder='templates',
    static_folder='static'
)


@idea_getgroupbytag_bp.route('/idea/get_group_by_tag', methods=['POST'])
def get_relevant_ideas():
    """/idea/get_group_by_tag"""
    # tag = request.args.get('tag').lower().replace("\'", "").replace('\"', "")
    tag = request.form.get('tag').lower().replace("\'", "").replace('\"', "")

    for idea_group in app.ideas:
        for idea in idea_group['ideas']:
            if tag.lower() in idea['tags']:
                return '{"result": true, "data": ' + str(idea_group).replace("\'", "\"") + '}'

    return str(BaseResponse(False, []))

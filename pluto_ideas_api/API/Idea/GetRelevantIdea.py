# -*- coding: utf-8 -*-
import json

import flask
from flask import current_app as app, request

from pluto_ideas_api.Classes.BaseResponse import BaseResponse
from pluto_ideas_api.Classes.textprocess.most_relevant_bm25_lematized import get_relevance_list

# Blueprint Configuration
idea_getrelevantideas_bp = flask.Blueprint(
    'relev_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@idea_getrelevantideas_bp.route('/idea/get_relevant_ideas', methods=['POST'])
def get_relevant_ideas():
    """/idea/get_relevant_ideas"""
    text_json = request.json

    if "text" in text_json:
        text = text_json["text"]

        result = get_relevance_list(text, app.ideas, app.predictor)

        relev_dict = {}
        for response in result:
            if response[0] in relev_dict:
                if response[2] > relev_dict[response[0]][1]:
                    relev_dict[response[0]] = (response[0], response[1], response[2])
            else:
                relev_dict[response[0]] = (response[0], response[1], response[2])

        group_list = list(relev_dict.values())
        group_list.sort(key=lambda x: x[2], reverse=True)

        groups = []
        for t in group_list[:5]:
            group = {}
            for idea in app.ideas:
                if idea['id'] == t[0]:
                    group = idea

            rel_text = ""
            for idea in group['ideas']:
                if idea['id'] == t[1]:
                    rel_text = idea['text']
            group['rel_text'] = rel_text

            groups.append(group)
        return json.dumps({'result': 'true', 'groups': groups})
    return '{"result": false, "data": []}'

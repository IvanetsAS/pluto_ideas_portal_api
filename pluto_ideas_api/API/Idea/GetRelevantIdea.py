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
    responce = request.form.get('text')
    # responce = "Музыка должна быть лучше!"

    result = get_relevance_list(responce, app.ideas, app.predictor)

    relev_dict = {}
    for responce in result:
        if responce[0] in relev_dict:
            if responce[2] > relev_dict[responce[0]][1]:
                relev_dict[responce[0]] = (responce[0], responce[1], responce[2])
        else:
            relev_dict[responce[0]] = (responce[0], responce[1], responce[2])

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

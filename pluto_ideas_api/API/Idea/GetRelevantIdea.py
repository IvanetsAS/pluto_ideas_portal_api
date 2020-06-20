# -*- coding: utf-8 -*-

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


@idea_getrelevantideas_bp.route('/idea/get_relevant_ideas', methods=['GET'])
def get_relevant_ideas():
    """/idea/get_relevant_ideas"""
    # TODO разобраться, как мы получаем текст
    # text = request.args.get('id')
    text = "Музыка должна быть лучше!"

    result = get_relevance_list(text, app.ideas, app.predictor)
    # TODO решить, в каком виде мы возвращаем результат
    return result

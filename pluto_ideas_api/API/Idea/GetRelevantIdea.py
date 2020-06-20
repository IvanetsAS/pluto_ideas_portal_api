# -*- coding: utf-8 -*-

import flask
from flask import current_app as app, request
from pluto_ideas_api.Classes.BaseResponse import BaseResponse

# Blueprint Configuration
idea_getrelevantideas_bp = flask.Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@idea_getrelevantideas_bp.route('/idea/get_relevant_ideas', methods=['GET'])
def get_relevant_ideas():
    """/user/get_user"""
    id = request.args.get('id')

    #HERE WIIL BE THE CONNECTION TO THE MODEL

    return "Здесь будет метод получение релевантных идей"
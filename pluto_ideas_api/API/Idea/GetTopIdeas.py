# -*- coding: utf-8 -*-
import json

import flask
from flask import current_app as app, request

from pluto_ideas_api.Classes.BaseResponse import BaseResponse

# Blueprint Configuration
idea_gettopideas_bp = flask.Blueprint(
    'gettopideas', __name__,
    template_folder='templates',
    static_folder='static'
)


@idea_gettopideas_bp.route('/idea/get_top_ideas', methods=['GET'])
def get_group_by_tag():
    """/idea/get_group_by_tag"""
    # tag = request.args.get('tag').lower().replace("\'", "").replace('\"', "")

    min_idea_rating = 999999
    top_ideas = {}
    for idea_group in app.ideas:
        for idea in idea_group['ideas']:

            current_idea_rating = idea["rating"]

            if len(top_ideas) <= 20:
                if current_idea_rating < min_idea_rating:
                    min_idea_rating = current_idea_rating
                top_ideas.update({current_idea_rating: idea})
            else:
                if current_idea_rating > min_idea_rating:
                    top_ideas.pop(min_idea_rating)
                    top_ideas.update({current_idea_rating: idea})
                    min_idea_rating = min(top_ideas.keys())

    ideas = list(top_ideas.values())
    ideas.sort(key=lambda n: n["rating"], reverse=True)

    return '{"result": true, "data": ' + str(ideas).replace("\'", "\"") + '}'


@idea_gettopideas_bp.after_request
def add_cors_headers(response):
    if request.referrer is not None:

        r = request.referrer[:-1]
        white = ['http://localhost:3000', 'http://localhost:8080']

        if r in white:
            response.headers.add('Access-Control-Allow-Origin', r)
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
            response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
            response.headers.add('Access-Control-Allow-Headers', 'Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    return response

# -*- coding: utf-8 -*-
import json
import os

from pymorphy2 import MorphAnalyzer
from flask import Flask, current_app, request

from pluto_ideas_api.Classes.User import User

"""Initialize Flask app."""


def create_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')

    with app.app_context():
        # Import parts of our application
        from pluto_ideas_api.API.User import GetUser
        from pluto_ideas_api.API.User import GetUsersRating
        from pluto_ideas_api.API.Idea import GetRelevantIdea
        from pluto_ideas_api.API.Idea import GetGroupByTag
        from pluto_ideas_api.API.Idea import GetTopGroups
        from pluto_ideas_api.API.Tags import GetTagsRating
        # Register Data
        with open(os.path.join('data', 'users.json'), encoding='UTF-8') as file:
            current_app.users = json.load(file)
        current_app.current_user = current_app.users[0]
        with open(os.path.join('data', 'data.json'), encoding='UTF-8') as file:
            current_app.ideas = json.load(file)
        current_app.predictor = MorphAnalyzer()

        # Register Blueprints
        app.register_blueprint(GetUser.user_getuser_bp)
        app.register_blueprint(GetUsersRating.tag_getusersrating_bp)
        app.register_blueprint(GetRelevantIdea.idea_getrelevantideas_bp)
        app.register_blueprint(GetTopGroups.idea_gettopgroups_bp)
        app.register_blueprint(GetGroupByTag.idea_getgroupbytag_bp)
        app.register_blueprint(GetTagsRating.tag_gettagsrating_bp)
        return app


if __name__ == "__main__":
    app = create_app()
    app.run()


    @app.after_request
    def add_cors_headers(response):
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

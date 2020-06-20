# -*- coding: utf-8 -*-


from flask import Flask, current_app

from pluto_ideas_api.Classes.User import User

"""Initialize Flask app."""


def create_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        # Import parts of our application
        from pluto_ideas_api.API.User import GetUser

        # Register Data
        current_app.current_user = User(
            1,
            "Алекандр",
            "Сергеевич",
            "Иванец",
            "картинка",
            "Ярославль",
            "Управление трехмерного моделирование",
            ".net разработчик",
            "89052668317",
            "ivanetcas@polymetal.ru",
            ["Ачивка 1", "Ачивка 2", ],
        )
        current_app.ideas = []

        # Register Blueprints
        app.register_blueprint(GetUser.user_getuser_bp)

        return app


if __name__ == "__main__":
    app = create_app()
    app.run()

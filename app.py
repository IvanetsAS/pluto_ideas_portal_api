from flask import Flask, app, current_app

from Classes.User import User

"""Initialize Flask app."""


def create_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        # Import parts of our application
        from API.User import GetUser


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
            ["Ачивка 1","Ачивка 2",],
        )

        # Register Blueprints
        app.register_blueprint(GetUser.user_getuser_bp)

        return app


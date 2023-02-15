import logging
import signal
import os

from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_apscheduler import APScheduler

from gpiozero import Button

db = SQLAlchemy()
bootstrap = Bootstrap()
scheduler = APScheduler()

def create_app():
    app = Flask(__name__)

    app.config.from_object("project.config.Config")

    db.init_app(app)
    bootstrap.init_app(app)

    app.gpio_button = Button(17)

    scheduler.init_app(app)
    from .main import twilio_sms_poll_job
    from .main import gpio_player_job
    scheduler.start()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # # Background thread test
    # @app.route('/task', methods=['POST', "GET"])
    # def submit_task():
    #     #print('test')
    #     #task = request.json
    #     #logging.info(f'Received task: {task}')
    #     logging.info(f'adding a task')
    #
    #     TASKS_QUEUE.put('some_task')
    #     print(TASKS_QUEUE)
    #     return jsonify({'success': 'OK'})
    # #
    # notification_thread = BackgroundThreadFactory.create('notification')
    # notification_thread.start()
    # logging.info(f'blocked ???')
    # print("end of create_app")
    # #
    # this condition is needed to prevent creating duplicated thread in Flask debug mode
    # if not (app.debug or os.environ.get('FLASK_ENV') == 'development') or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    #     notification_thread.start()
    #
    #     original_handler = signal.getsignal(signal.SIGINT)
    #
    #     def sigint_handler(signum, frame):
    #         notification_thread.stop()
    #
    #         # wait until thread is finished
    #         if notification_thread.is_alive():
    #             notification_thread.join()
    #
    #         original_handler(signum, frame)
    #
    #     try:
    #         signal.signal(signal.SIGINT, sigint_handler)
    #     except ValueError as e:
    #         logging.error(f'{e}. Continuing execution...')


    return app


app = create_app()




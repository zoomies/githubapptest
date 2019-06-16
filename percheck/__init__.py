import os
import logging
from flask import Flask
from dotenv import load_dotenv

logging.basicConfig(filename='percheck.log', level=logging.INFO, format= '%(asctime)s - %(module)s: %(levelname)s: %(message)s')


load_dotenv()

def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.logger.info("Initializing App")

    if str(os.getenv("PRIVATE_KEY")) != 'None':
        app.config['PRIVATE_KEY']=os.getenv("PRIVATE_KEY")
    else:
        app.logger.error("Private Key Not Loaded")

    if str(os.getenv("GITHUB_APP_IDENTIFIER")) != 'None':
        app.config['GITHUB_APP_IDENTIFIER']=os.getenv("GITHUB_APP_IDENTIFIER")
    else:
        app.logger.error("Github App ID Not Loaded with load_dotenv")

    if str(os.getenv("GITHUB_WEBHOOK_SECRET")) != 'None':
        app.config['GITHUB_WEBHOOK_SECRET']=os.getenv("GITHUB_WEBHOOK_SECRET")
    else:
        app.logger.error("Github Webhook Secret Not Loaded with load_dotenv")

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from percheck import (hello, webhook)
    app.register_blueprint(hello.bp)
    app.register_blueprint(webhook.bp)
    return app

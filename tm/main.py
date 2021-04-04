import tm
from tm.utils.containers import (
    auth
)
from flask import Flask
from mongoengine import connect
from flask_smorest import Api
from tm.auth.routes import auth_blp
import os
from manage import (
    create_super_admin
)
import sys
from celery import Celery
from dotenv import (
    load_dotenv
)

load_dotenv(dotenv_path=".flaskenv")

MONGO_HOST = os.environ["MONGO_HOST"]
MONGO_PORT = int(os.environ["MONGO_PORT"])
MONGO_USERNAME = os.environ["MONGO_USERNAME"]
MONGO_PASSWORD = os.environ["MONGO_PASSWORD"]
REDIS_BROKER_URL = os.environ["REDIS_BROKER_URL"]

celery = Celery(__name__, broker=REDIS_BROKER_URL)


def create_app(config_filename):

    conn = connect(
        'tm',
        host=MONGO_HOST,
        port=MONGO_PORT,
        username=MONGO_USERNAME,
        password=MONGO_PASSWORD
    )

    # dependency injection containers
    token_user_container = auth.TokenUserContainer()
    token_user_container.wire(packages=[tm])

    app = Flask(__name__)

    app.db = conn

    app.config['API_TITLE'] = 'Tuition Management API'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.2'
    app.config['OPENAPI_JSON_PATH'] = 'api-spec.json'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_REDOC_PATH'] = '/redoc'
    app.config['OPENAPI_REDOC_URL'] = 'https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/docs'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    app.config['API_SPEC_OPTIONS'] = {
        'components': {
            "securitySchemes":
                {
                    "OAuth2PasswordBearer": {
                        "type": "oauth2",
                        "flows": {
                            "password": {
                                "scopes": {},
                                "tokenUrl": "/auth/"
                            }
                        }
                    }
                }
        }
    }
    app.config['CELERY_BROKER_URL'] = REDIS_BROKER_URL
    app.config['MONGODB_CONNECT'] = False

    celery.conf.update(app.config)

    # * cli commands
    app.cli.add_command(create_super_admin)

    api = Api(app)
    api.register_blueprint(auth_blp)
    return app

import logging
import logging.handlers

from flask import Flask


def create_app(name):
    logging.basicConfig(level=logging.INFO,
                        format="%(threadName)s %(asctime)s %(name)-12s %(message)s",
                        datefmt="%d-%m-%y %H:%M")

    app = Flask(name)
    return app

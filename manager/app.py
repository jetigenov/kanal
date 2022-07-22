# coding=utf-8
import logging
import traceback

from flask import Response, request, render_template
from flask_cors import CORS

from flask_migrate import Migrate

from manager import service
from db_home.models import db, Order
from lib import AppFactory
from lib.codes import SYSTEM_ERROR
from lib.utils import BusinessException, make_json_response, orm_to_json

app = AppFactory.create_app(__name__)
app.config.from_object('config.settings')


CORS(app, headers=['Content-Type', 'Authorization'])
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/', methods=['GET'])
def home():

    data = db.session.query(Order).all()
    context = orm_to_json(data)

    return render_template('home.html', context=context)


@app.errorhandler(BusinessException)
@app.errorhandler(Exception)
def core_error(e):
    code = ''
    if hasattr(e, 'code'):
        code = str(e.code)
    logging.error(traceback.format_exc() + code)
    db.session.rollback()
    if isinstance(e, BusinessException):
        return make_json_response({'result': e.code, 'message': e.message})
    if isinstance(e, KeyError):
        return make_json_response(
            {'result': -20,
             'message': u'Обязательный параметр отсутствует: ' + str(e)})
    return make_json_response({'result': SYSTEM_ERROR})


@app.route("/manager/<string:path>/<string:command>", methods=['POST'])
@app.route("/manager/<string:path>.<string:command>", methods=['POST'])
def catcher(path, command):
    data = request.json or {}

    response = service.call(f'{path}.{command}', data)

    if isinstance(response, Response):
        return response

    return make_json_response(response)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5050)
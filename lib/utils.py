import decimal
import json
from copy import copy
import datetime

from flask import g, Response
from sqlalchemy.orm import DeclarativeMeta

from lib.codes import MESSAGES


class JSONEncoderCore(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            r = str(o)[:19]
            return r
        elif isinstance(o, datetime.date):
            return str(o)
        elif isinstance(o, datetime.time):
            r = str(o)
            return r
        elif isinstance(o, decimal.Decimal):
            return fakefloat(o)
        elif isinstance(o, datetime.timedelta):
            return o.total_seconds()
        elif isinstance(o.__class__, DeclarativeMeta):
            return orm_to_json(o)
        else:
            return super(JSONEncoderCore, self).default(o)


class fakefloat(float):
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return str(self._value)


def orm_to_json(orm):
    if not orm:
        return None
    if isinstance(orm, list):
        ret = []
        for o in orm:
            if hasattr(o, '__dict__'):
                d = copy(o.__dict__)
            else:
                d = o._asdict()
            d.pop('_sa_instance_state', None)
            ret.append(d)
        return ret
    else:
        if hasattr(orm, '__dict__'):
            d = copy(orm.__dict__)
        else:
            d = orm._asdict()
        d.pop('_sa_instance_state', None)
        return d


def make_json_response(p_content, status=200):
    if not p_content:
        p_content = {}
    if 'result' not in p_content:
        p_content.update({'result': 0})

    if p_content['result'] == 0:
        status = 200
    elif p_content['result'] == -1:
        status = 500
    elif p_content['result'] == -15:
        status = 401
    elif p_content['result'] in [-16, -17]:
        status = 403
    else:
        status = 405

    json_string = json.dumps(p_content, cls=JSONEncoderCore)
    resp = Response(
        json_string, mimetype='application/json; charset=utf-8', status=status)
    return resp


def make_json_response_200(p_content):
    if not p_content:
        p_content = {}
    if 'result' not in p_content:
        p_content.update({'result': 0})

    json_string = json.dumps(p_content, cls=JSONEncoderCore)
    resp = Response(json_string, mimetype='application/json; charset=utf-8')
    return resp


class BusinessException(Exception):
    def __init__(self, code, message=None):
        super(BusinessException, self).__init__()
        self.code = code
        self.message = message
        if not message:
            self.message = MESSAGES.get(g.language, {}).get(
                code, f'pytНеизвестная ошибка: {code}')

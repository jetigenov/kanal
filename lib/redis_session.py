from uuid import uuid1
from datetime import timedelta
from redis import Redis
from config.settings import REDIS_URI, REDIS_DB

SESSION_TIMEOUT = 60


def open_session(token):
    redis = Redis(REDIS_URI, db=REDIS_DB)
    sid = str(uuid1(clock_seq=redis.incr('session_id')))
    redis.setex('session:' + sid, timedelta(minutes=SESSION_TIMEOUT), token)
    return sid


def get_session(sid):
    redis = Redis(REDIS_URI, db=REDIS_DB)
    data = redis.get('session:' + sid)
    if data:
        redis.setex('session:' + sid, timedelta(minutes=SESSION_TIMEOUT), data)
        data = data.decode()
    return data

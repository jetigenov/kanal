from lib.codes import OBJECT_DOES_NOT_EXIST
from lib.utils import BusinessException


def get_obj(session, model, obj_id):
    """
    Для получения объекта в базе по id иначе выдаст ошибку объект отсутствует в базе
    """
    obj = session.query(model).filter(model.id == obj_id).first()

    if not obj:
        raise BusinessException(code=OBJECT_DOES_NOT_EXIST)

    return obj

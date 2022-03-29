
import time
import json
import logging

from typing import Any, Union


class SelfJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if not isinstance(obj, (dict, list, tuple, str, int, float, type(None))):
            if isinstance(obj, set):
                return list(obj)
            try:
                return str(obj)
            except:
                return "Can't convert obj to str."
        return super().default(obj)


def convert_log_to_dict(title: str, data: Any, message: str = "", err: Union[BaseException, str] = "") -> str:
    return json.dumps({
        "title": title,
        "err_msg": str(err),
        "data": data,
        "message": message,
        "time": str(time.time())
    }, cls=SelfJSONEncoder)


def error_gather(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(
                convert_log_to_dict(
                    func.__name__,
                    {'args': args, 'kwargs': kwargs},
                    err=e
                )
            )
            raise e
    return wrapper

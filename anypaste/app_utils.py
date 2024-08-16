from datetime import datetime, date
from collections.abc import Iterable
from decimal import Decimal
from json import dumps


async def jd(d, from_db=False):
    async def handle_datetime(obj):
        if isinstance(obj, str):
            return obj
        elif isinstance(obj, dict):
            return {k: await handle_datetime(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [await handle_datetime(item) for item in obj]
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return obj

    if from_db:
        d = [dict(rec) for rec in d]
    return dumps(await handle_datetime(d), indent=4, ensure_ascii=False)



async def accummulator(incoming_payload, inner_func):
    payload = incoming_payload

    async def wrapper_func(**kwargs):
        nonlocal payload
        updated_payload = await inner_func(payload, **kwargs)
        if isinstance(updated_payload, dict):
            payload = {**updated_payload}
        return payload.get('result', None)

    return wrapper_func


async def is_null(X):
    if X is None:
        return X
    
    if (
        isinstance(X, Iterable) and
        not isinstance(X, str)
    ):
        single_case = False
        try:
            is_len_null = len(X) == 0
            if len(X) == 1:
                single_case = True
        except Exception as e:
            is_len_null = False

        if X is None or is_len_null:
            return True

        try:
            if (
                single_case and not isinstance(X, dict) and
                str(X[0]).lower().strip() in ['none', '', 'null']
            ):
                return True
        except KeyError:
            return False

        return False
    # Make a copy:
    _x = '' + str(X)

    if _x.lower().strip() in ['none', '', 'null']:
        return True
    return False

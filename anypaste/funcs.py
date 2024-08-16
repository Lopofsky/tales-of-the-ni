from asyncio import sleep as async_sleep
from re import sub as re_sub
from operator import mul, add, sub, truediv, pow
from math import factorial

# App imports:
from app_utils import is_null, jd
from db_utils import AsyncContextDB


async def get_rms_id(payload, **kwargs):
    mapping = {
        'a': ['receipts', 'APY'],
        'ea': ['ef_receipts', 'External_APY'],
        't': ['invoices', 'TPY'],
        'et': ['ef_invoices', 'External_TPY'],
        'c': ['creditnote', 'CR'],
    }
    keys2unwrap = ['expr', 'year', 'hotel', 'doc_type',]
    
    (
        doc_enum,
        year,
        hotel,
        doc_type,
    ) = [
        kwargs.get(x) 
        for x in keys2unwrap
    ]
    
    doc_type = mapping.get(doc_type)
    db_name = hotel + year
    async with AsyncContextDB(server='rms', database_name=db_name) as conn:
        # Perform your database operations
        query = f"""
            SELECT i."ID"
            FROM "{doc_type[0]}" i
            WHERE i."Enumeration"='{doc_enum}'
        """
        result = await conn.fetch(query)
        doc_id = result[0]['ID']
        result = f"https://user.com/doc_id={doc_id}&category={doc_type[1]}"
    payload.update({'result': result})
    return payload


def clean_text(text):
    cleaned = re_sub(r'[^a-zA-Z\s]', ' ', text)
    cleaned = re_sub(r'\s+', ' ', cleaned)
    cleaned = cleaned.replace(' ', '_')
    return cleaned.strip()


async def sql_repl(payload, **kwargs):
    ENDFIX = '.sql'
    sql_filename = kwargs.get('expr')
    if await is_null(sql_filename):
        sql_filename = 'exp' + ENDFIX
    
    # Uneccessary: Just there to cover the linter:
    if sql_filename is None:
        raise Exception("""
            `payload['expr`]` (aka `sql_filename`)
            can't be None!
        """)
    
    if ENDFIX not in sql_filename:
        sql_filename += ENDFIX
        
    repla = {
        '{year}': '2024',
        '{STARTO}': '05-01',
        '{ENDO}': '10-21',
        '__GUARANTEE_VALUES__': "('kamari', 50)",
        '__GUARANTEE_CONTRACTS__': "999999"
    }
    
    with open(sql_filename) as f:
        query = f.read()
    
    for k, replacor in repla.items():
        query = query.replace(k, replacor)
    
    payload['result'] = query
    return payload


async def adder(payload, **kwargs):
    if (
        'expr' not in kwargs.keys() or
        not all([
            x in ['current_sum', 'previous_result'] or x == 'result'
            for x in payload.keys()
        ])
    ):
        raise Exception("@`adder`: missing payload or kwargs!")

    expr = kwargs['expr']
    possible_operation = expr[0]

    if possible_operation == '!':
        payload['current_sum'] = factorial(int(payload['current_sum']))
        payload.update({'result': payload['current_sum']})
        return payload

    if possible_operation == '~':
        payload['current_sum'] = payload['previous_result']
        expr = expr[1:]
        if len(expr) > 1:
            possible_operation = expr[0]
    else:
        payload['previous_result'] = payload['current_sum']

    operation = {
        '+': add,
        '-': sub,
        '*': mul,
        '/': truediv,
        '^': pow,
    }.get(possible_operation)

    if operation is None:
        operation = add
    else:
        expr = expr[1:].replace('-', '')

    try:
        expr = float(expr)
        payload['current_sum'] = round(
            operation(payload['current_sum'], expr), 2
        )
    except Exception as e:
        if hasattr(expr, '__len__') and len(expr) > 0:
            print(f'{expr=} IS NOT A VALID NUMERIC! {e=}')

    payload.update({'result': payload['current_sum']})
    return payload

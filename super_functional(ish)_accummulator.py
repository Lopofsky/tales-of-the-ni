# Init Source & Credits: https://stackoverflow.com/questions/49046554/function-that-returns-an-accumulator-in-python

from collections.abc import Iterable

def make_accumulator(primitive=dict, str_decor={'pre':'>', 'end':'<'}):
    types = {'str':'', 'int':0, 'float':0.0, 'list':[], 'dict':{}}
    what, init = (primitive, False) if type(primitive) is type else (type(primitive), True)
    so_far = types.get(what.__name__, None)
    if so_far is None: raise Exception(f"{primitive=} Type Is Not Yet Supported!")
    if init: so_far = primitive
    if what.__name__ == 'dict':
        if type(str_decor) is not dict: raise Exception("'str_decor' is not a dict!")
        str_decor = {x:str_decor.get(x, '') for x in ['pre', 'end']}
        def accumulate(k, v=None):
            nonlocal so_far
            invalid_conditions = {"1 arg, but not dict":(v is None and not isinstance(k, dict)),
            "2 args, but with iterable key":(v is not None and isinstance(k, Iterable) and not isinstance(k, str))}
            if sum(list(invalid_conditions.values())) > 0:
                raise Exception(f""" {invalid_conditions=}
                    False args! Proper options:
                    #0 : obj(<Non-Iterable>, <T>) -> dict
                    #1 : obj(dict) -> dict """)
            if k not in so_far: so_far[k] = v
            else:
                if type(v) is dict: so_far[k].update(v)
                elif type(v) is str: so_far[k] += str_decor['pre']+v+str_decor['end']
                else:
                    try: so_far[k] += v
                    except Exception as e: 
                        raise Exception('<'+str(e)+'>')
            return so_far
    else:
        def accumulate(x):
            nonlocal so_far
            try: so_far += x
            except Exception as e: 
                raise Exception('<'+str(e)+'>')
            return so_far
    return accumulate

acc = make_accumulator()
acc('a', 6) ; acc('b', 'asd') ; z = acc('d', {1:2})
print(z)

acc2 = make_accumulator(int) # or: make_accumulator(0)
acc2(32) ; z = acc2(43)
print(z)

acc3 = make_accumulator(str) # or: make_accumulator('')
acc3("Άλφα") ; acc3(" ρε") ; acc3(" γαβ"*2)
print(acc3("!"))

acc3_2 = make_accumulator("Άλφα")
acc3_2(" ρε") ; acc3_2(" γαβ"*2)
print(acc3("!"))

acc4 = make_accumulator([]) # or: make_accumulator(list) | or: make_accumulator([1,2,3])
acc4([1,2,3])
print(acc4(['ena', 'diop']))


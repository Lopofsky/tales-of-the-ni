'''
KUDOS & SERIOUS CREDITS TO Mr. Martin McBride, his two articles below allowed me to expand the Monad class to this extend and make it a really useful tool to assist me in using functional style on my code:
-----------------------------------------------------------------------------------------
# The List Monad: https://medium.com/swlh/more-monads-in-python-178492f482f6
# The Failure Monad: https://medium.com/swlh/monads-in-python-e3c9592285d6
-----------------------------------------------------------------------------------------
'''
from functools import reduce

class Monad():

    def __init__(self, value, Success=True): 
        self.value, self.Success, self.type = value, Success, type(value)
        self.is_dict, self.is_list, self.is_iterable = isinstance(value, dict), isinstance(value, list),  hasattr(value, '__iter__')
        self.default_rdc_types = {
            float : 0.0,
            int : 0,
            str : '',
            list : [],
            dict : {},
            tuple : ()
        }

    def __str__(self): return str(self.value)

    def __call__(self): return self.value

    def __or__(self, f): return self.x(f)

    def __sub__(self, f, rdc=True): 
        # Reduce based only on values:
        if self.is_iterable: 
            if isinstance(f, list): return self.x(f[0], kv=self.is_dict, rdc=f[1])
            return self.x(f, kv=self.is_dict, rdc=rdc)
        else: raise Exception(f"YOU CAN'T USE THE __sub__ OPERATOR (`-`) WITHOUT ITERABLE PAYLOAD! {type(self.value)=} ")

    def __truediv__(self, f): 
        # Reduce based only on key & values (requires init payload to be a dict):
        if self.is_iterable and isinstance(f, list): return self.__sub__(f[0], rdc=f[1])
        else: raise Exception(f"YOU CAN'T USE THE __pow__ OPERATOR (`/`) WITHOUT A LIST AS A RIGHT HAND ARGUMENT, WITH THE FOLLOWING STRUCTURE: ` (monad_obj) / [(f, arg1, ..., argn), INIT_REDUCER] ` AND AN ITERABLE AS THE LEFT HAND (aka self.value for the monad_obj)! {type(self.value)=} ")

    def __add__(self, f): 
        if self.is_dict: return self.x(f, kv=True)
        else: raise Exception(f"YOU CAN'T USE THE __add__ OPERATOR (`+`) WITHOUT DICT PAYLOAD! {type(self.value)=} ")

    def is_Success(self): return self.Success

    def unpack_function(self, f, kv, rdc=False):
        multi_arg_expand = {
            (True, False) : lambda k, v : f[0](k, v, *f[1:]), 
            (False, False) : lambda x : f[0](x, *f[1:]),
            (False, True) : lambda acc, curr : f[0](acc, curr, *f[1:]),
            (True, True) : lambda acc, kv_pair : f[0](acc, kv_pair, *f[1:]) # It's the same as the `(False, True)` case, I've just renamed the 2nd arg to 'kv_pair', to clarify that this is a tuple with the key-value pair of each record of the dictionary payload (self.value).
        }
        return multi_arg_expand.get((kv, rdc is not False)) if isinstance(f, tuple) else f

    def x(self, f, kv=False, rdc=False):# aka `bind`
        if not self.Success: return self
        try:
            r, ff = self(), self.unpack_function(f, kv, rdc)
            options = {
                (list, True,):(lambda fx, r: Monad(map(fx, r)) | list), 
                (dict, True,):(lambda fx, r: Monad({
                        k:(
                            (Monad(v) + fx) if kv 
                            else (Monad(v) | fx)
                        )()
                        if isinstance(v, dict) 
                        else fx(k,v) if kv else fx(v)
                        for k, v in r.items()
                        }
                    )
                )
            }
            if rdc is not False:
                if self.is_dict: 
                    if rdc is True or kv is False:
                        r = list(r.values())
                        rdc_type = type(r[0])
                    else: 
                        r = [(k, v) for k,v in r.items()]
                        rdc_type = type(r[0][1])
                elif self.is_list:
                    rdc_type = type(r[0])
                else:
                    rdc_type = type(r)
                if rdc == True:
                    rdc = self.default_rdc_types.get(rdc_type)
                return Monad(reduce(ff, r, rdc))
            return options.get((type(r), self.Success,), lambda x,y:False)(ff, r) or Monad(ff(r))
        except Exception as e: 
            msg = ''
            if str(e).find("<lambda>() missing 1 required positional argument:")>-1 and not kv:
                msg = "Try enclosing the whole left expression in a parenthesis and use '+' instead of '|'."
            res = Monad({f.__name__  if not isinstance(f, tuple) else str(type(f)):str(e), 'Help Message':msg}, False)
            return res


if __name__ == "__main__":

    a = Monad(5)
    add_one = lambda x: x + 1
    add_more = lambda x, y: x + y
    a = a | add_one | (add_more, 5) | (lambda x: x+2)
    print(f"Case #0: {a()=}")

    mrep = lambda ss, dd, rr='': (ss if not dd else mrep(ss.replace(dd.pop(), rr), dd, rr)) if type(ss)==str else ss
    two2one_args_lambda = lambda x: mrep(x, ['just a string:', '-'])
    meaningless = lambda x: 'just a string:'+str(x) if type(x) in (int, float) else str(x)+'-0'
    payload = {'a':1, 'b':2.09, 'c':3.236, 
        'd':{
            4:{55:'0.25'}
            }
    }

    # DICT MONAD -> Example for accessing k,v with the right operant (LEFT OPERANT HAS TO BE A DICT MONAD!!!!): `(Monad(payload) | func1) + two_arg_func_that_wants_to_access_dict_keys_as_well`.
    # [NOTICE]: The result always affects only the `values` of the dict.

    meaningless_custom_filter = (lambda k,v: meaningless(v) if str(k) not in ('b', 'c') else v*10**9 )
    l = (Monad(payload) | two2one_args_lambda) + meaningless_custom_filter | two2one_args_lambda | float | int
    print(f"Case #1: {l()=}") # Also print(l) returns the str formatted value of self.value, but with f-strings we need to use the __call__ function of the Monad object.


    # Since the below function is returning a Monad, we have to call it before we return it, otherwise the inner lambda won't execute:

    dict_pay = {str(x):x if x<50 else {"inner":{"in2":x*9.63}} for x in range(1, 100+1)}
    mult_based_on_key = lambda k,v: (Monad(v)|(lambda x: x if k.isnumeric() and float(k)<35 else x*2.3)) ()
    gen = Monad(dict_pay) + mult_based_on_key | (lambda x: round(x, 4))
    print(f"Case #2: {gen()=}")

    # "Partialize" Multi arg functions:
    td = Monad({"a":1, "2":"two"})
    t = lambda k, v, a, b: v if k.isnumeric() else (v+a)*b
    t2 = lambda k, v, a, b: v if k.isnumeric() else (v-a)/b
    r = td + (t, 50, 49) + (t2, 2, 5)
    print(f"Case #3: {r()=}")

    # `reduce` (operator '*' overloaded) with partializing custom function on a list:
    e = Monad([x for x in range(1, 100+1)])
    f1 = lambda x: x + 1
    f2 = lambda x, y, z, q: x + y + z - q
    # Parentheses around all the previous expressions are necessary for the '-' operator:
    result = (e | f1) - (f2, 5, 10)
    print(f"Case #4: {result()=}")

    # `reduce` (operator '/' overloaded) with partializing custom function on a dict & accessing both keys & values. Init Value is mandatory, due to the tupple type:
    ff2 = lambda acc, rec, extra : (acc + rec[1] + extra) #if rec[0]%2==0 else 0
    conv = lambda x, m, r: x*x if x%m==r else x*x
    a = Monad({x:x for x in range(1, 101)})
    za = (a | (conv, 2, 0)) / [(ff2, 10), 0]
    print(f"Case #5: {za()=}")

    # Same as the above example, only difference is the usage of '-' operator, where the right hand expression has access only at the values of the dict (monad_obj.value) & this time we use a custom initial value for the reducing (-1000). 
    e = Monad([x for x in range(1, 100+1)])
    f1 = lambda x: x + 1
    f2 = lambda x, y, z, q: x + y + z - q
    res = (e | f1) - [(f2, 5, 10), -1000] 
    print(f"Case #6: {res()=}")
'''
KUDOS & SERIOUS CREDITS TO Mr. Martin McBride, his two articles below allowed me to expand the Monad class to this extend and make it a really useful tool to assist me in using functional style on my code:
-----------------------------------------------------------------------------------------
# The List Monad: https://medium.com/swlh/more-monads-in-python-178492f482f6
# The Failure Monad: https://medium.com/swlh/monads-in-python-e3c9592285d6
-----------------------------------------------------------------------------------------
'''

class Monad():
    def __init__(self, value, Success=True): self.value, self.Success = value, Success
    def __str__(self): return str(self.value)
    def __call__(self): return self.value
    def __or__(self, f): return self.x(f)
    def __add__(self, f): 
        if type(self.value) == dict: return self.x(f, kv=True)
        else: raise Exception(f"YOU CAN'T USE THE __add__ OPERATOR (`+`) WITHOUT DICT PAYLOAD! {type(self.value)=} ")
    def is_Success(self): return self.Success
    def x(self, f, kv=False):# aka `bind`
        if not self.Success: return self
        try: 
            r = self()
            if isinstance(f, tuple):
                multi_arg_expand = {True:(lambda k, v : f[0](k, v, *f[1:])), False:(lambda x : f[0](x, *f[1:]))}
                ff = multi_arg_expand.get(kv, None)
            else: ff = f#dc(f)
            options = {
                (list, True,):(lambda fx, r: Monad(map(fx, r)) | list), 
                (dict, True,):(lambda fx, r: Monad({
                        k:(
                            (Monad(v) + fx) if kv 
                            else (Monad(v) | fx)
                        )()
                        if type(v)==dict 
                        else fx(k,v) if kv else fx(v)
                        for k, v in r.items()
                        }
                    )
                )
            }
            return options.get((type(r), self.Success,), lambda x,y:False)(ff, r) or \
            Monad(ff(r))
        except Exception as e: 
            msg = ''
            if str(e).find("<lambda>() missing 1 required positional argument:")>-1 and not kv:
                msg = "Try enclosing the whole left expression in a parenthesis and use '+' instead of '|'."
            res = Monad({f.__name__  if not isinstance(f, tuple) else 'type(f)':str(e), 'Help Message':msg}, False)
            return res

mrep = lambda ss, dd, rr='': (ss if not dd else mrep(ss.replace(dd.pop(), rr), dd, rr)) if type(ss)==str else ss
two2one_args_lambda = lambda x: mrep(x, ['Pente:', '-'])
meaningless = lambda x: 'Pente:'+str(x) if type(x) in (int, float) else str(x)+'-0'
payload = {'a':1, 'b':2.09, 'c':3.236, 
    'd':{
        4:{55:'0.25'}
        }
}

# DICT MONAD -> Example for accessing k,v with the right operant (LEFT OPERANT HAS TO BE A DICT MONAD!!!!): `(Monad(payload) | func1) + two_arg_func_that_wants_to_access_dict_keys_as_well`.
# [NOTICE]: The result always affects only the `values` of the dict.

meaningless_custom_filter = (lambda k,v: meaningless(v) if str(k) not in ('b', 'c') else v*10**9 )
l = (Monad(payload) | two2one_args_lambda) + meaningless_custom_filter | two2one_args_lambda | float | int
print(l())


# Since the below function is returning a Monad, we have to call it before we return it, otherwise the inner lambda won't execute:

dict_pay = {str(x):x if x<50 else {"inner":{"in2":x*9.63}} for x in range(1, 100+1)}
mult_based_on_key = lambda k,v: (Monad(v)|(lambda x: x if k.isnumeric() and float(k)<35 else x*2.3)) ()
gen = Monad(dict_pay) + mult_based_on_key | (lambda x: round(x, 4))
print(gen())
# "Partialize" Multi arg functions:

td = Monad({"a":1, "2":"dio"})
t = lambda k, v, a, b: v if k.isnumeric() else (v+a)*b
t2 = lambda k, v, a, b: v if k.isnumeric() else (v-a)/b
r = td + (t, 50, 49) + (t2, 2, 5)
print(r())

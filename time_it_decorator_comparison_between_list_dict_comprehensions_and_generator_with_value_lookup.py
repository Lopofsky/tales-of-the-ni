from collections import namedtuple as nt
from sys import getsizeof
from time import time

def time_it(f):
	def tt(*args, **kw):
		t = time
		s, _, e = t(), f(*args, **kw), t()
		print(f">>> Timing: {f.__name__} -> {e-s}")
	return tt

########### [START] BAD #############################
@time_it
def dicto(max_r, find_key):
	mxr = max_r
	a, fk = {str(num+3.7):num**2 for num in range(1,mxr,1)}, find_key
	result = a[fk]
	print("dict lookup result ->", result)
	print("dict generated size ->", getsizeof(a))

@time_it
def listo(max_r, find_key):
	mxr = max_r
	b, fk = [(str(num+3.7), num**2) for num in range(1,mxr,1)], find_key
	result = [p[1] for p in b if p[0]==fk][0]
	print("list(tuple) lookup result ->", result)
	print("list(tuple) generated size ->", getsizeof(b))
########### [END] BAD ###############################


########### [START] OPTIMIZED #############################
@time_it
def gene(max_r, find_key, namedtuples=False):
	if not namedtuples:
		mxr = max_r
		regen = lambda mxr: ((str(num+3.7), num**2) for num in range(1,mxr,1)) # hacky: RESET GENERATOR TO RE-ITERATE / RE-YIELD
		c, fk = regen(mxr), find_key
		result = next(str(x[1]) for x in c if x[0] == fk)
		c = regen(mxr) # REGENERATE THE GENERATOR
		result = next(float(x[1]) for x in c if x[0] == fk)
		print("generator(simple_tuple) lookup result ->", result)
		print("generator(simple_tuple) generated size =", getsizeof(c))
	# namedtuple keeps the size same, *BUT* is slower the non-namedtuple generator variant @ lookup!!!
	else:
		mxr, r = max_r, nt("Record", "key value")
		regen = lambda mxr: (r(str(num+3.7), num**2) for num in range(1,mxr,1)) # hacky: RESET GENERATOR TO RE-ITERATE / RE-YIELD
		c, fk = regen(mxr), find_key
		result = next(str(x.value) for x in c if x.key == fk)
		c = regen(mxr) # REGENERATE THE GENERATOR
		result = next(float(x.value) for x in c if x.key == fk)
		print("generator(namedtuple) lookup result ->", result)
		print("generator(namedtuple) generated size =", getsizeof(c))
########### [END] OPTIMIZED ###############################

if __name__ == '__main__':
	mr, fk = 1000000, "8.7"
	dicto(mr, fk), listo(mr, fk), gene(mr, fk, namedtuples=True), gene(mr, fk, namedtuples=False)

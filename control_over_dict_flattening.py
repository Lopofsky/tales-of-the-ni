# Init Source & Credits: https://www.geeksforgeeks.org/python-convert-nested-dictionary-into-flattened-dictionary/
def flatten_dict(pyobj, prefix=True, keystring='', sep='.'):
    if type(pyobj) == dict:
        keystring = keystring + sep if keystring else keystring
        for k in pyobj:
            yield from flatten_dict(pyobj[k], prefix, (keystring + str(k)) if prefix else str(k), sep)
    else:
        yield keystring, pyobj


if __name__ == "__main__":
    b = {"t2":4, "p":5, "zzz":{"1":4, "2":44, "3":444}}
    r = dict(flatten_dict(b))
    print(r)

    r = dict(flatten_dict(b, prefix=False))
    print(r)
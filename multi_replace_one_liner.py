mrep = lambda ss, dd, rr='': (ss if not dd else mrep(ss.replace(dd.pop(), rr), dd, rr)) if type(ss)==str else ss

ss = "asd1 Porks Opas"
r = mrep(ss, ["pa", "Po"])
print(r)
r = mrep(ss, ["pa", "Po"], "XXXXX")
print(r)
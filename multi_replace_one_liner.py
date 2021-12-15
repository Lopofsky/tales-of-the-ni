mrep = lambda ss, dd, rr='': (ss if not dd else mrep(ss.replace(dd.pop(), rr), dd, rr)) if type(ss)==str else ss

if __name__ == "__main__":
    ss = "asd1 Porks Opas"
    r = mrep(ss, ["pa", "Po"])
    print(r)
    r = mrep(ss, ["pa", "Po"], "XXXXX")
    print(r)
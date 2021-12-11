from inspect import getframeinfo, currentframe, getouterframes

def super_print(presentation="|#count@line|--->", start=0, step=1):
    count = start

    def sp2(string):
        nonlocal count
        ln_cnt = str(getframeinfo(getouterframes(currentframe())[1][0]).lineno)
        print(presentation.replace("count", str(count)).replace("line", ln_cnt), string)
        count += step
        if not float(count).is_integer():
            check_str_format_due_to_exp_not_fucked_up_stuff = str(step) # https://stackoverflow.com/questions/38847690/convert-float-to-string-in-positional-format-without-scientific-notation-and-fa
            #print(f"{check_str_format_due_to_exp_not_fucked_up_stuff=}")
            round_factor = abs(int(check_str_format_due_to_exp_not_fucked_up_stuff)) if '1e-' in check_str_format_due_to_exp_not_fucked_up_stuff else len(str(step).split('.')[1])
            count = round(count, round_factor)
    return sp2

p = super_print()

a = "test"
p(f"This is a {a}")
p("Just print it")
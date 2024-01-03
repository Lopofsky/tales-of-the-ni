from datetime import datetime
from inspect import currentframe, getframeinfo


def super_print(
    active=True,
    presentation="|#count@line - time|---> result",
    start=0, step=1,
    suffix="\n", endfix="\n"
):
    count = start
    last_time = datetime.now()

    def format_presentation(line_number, input_string):
        current_time = datetime.now()
        time_diff = current_time - last_time
        time_str = f"{time_diff.seconds}.{time_diff.microseconds}"
        formatted_line = (
            presentation
            .replace("count", str(count))
            .replace("line", str(line_number))
            .replace("time", time_str)
            .replace("result", input_string)
        )
        if 'result' not in presentation:
            formatted_line += f': {input_string}'
        return formatted_line

    def print_logger(string="", active=active):
        nonlocal count, last_time
        if active:
            caller_frame = currentframe().f_back
            line_number = getframeinfo(caller_frame).lineno
            formatted_string = ''.join([
                suffix,
                format_presentation(line_number, str(string)),
                endfix
            ])
            print(formatted_string)

        count += step
        last_time = datetime.now()

    return print_logger


if __name__ == "__main__":
    # Example usage
    pp = super_print(active=True, presentation=">line@time: `result`")

    pp('start')
    a_dict = {'a': 1}
    pp(a_dict)

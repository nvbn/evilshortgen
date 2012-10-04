from byteplay import (
    Code, STORE_FAST, YIELD_VALUE,
    BINARY_LSHIFT, SetLineno, LOAD_FAST,
)
from functools import partial
from tornado import gen
import inspect

def shortgen(fnc):
    code = Code.from_code(fnc.func_code)
    pops = []
    line_num = 0
    source = inspect.getsourcelines(fnc)[0]
    for num, line in enumerate(source):
        if 'def' in line:
            break
    source = source[num + 1:]
    for num, line in enumerate(code.code):
        if num and SetLineno in code.code[num - 1]:
            if '<<' in source[line_num]:
                last = num, line
            line_num += 1
        if BINARY_LSHIFT in line:
            ls_num, ls_line, (lo_num, lo_line) = (
                num, line, last,
            )
            code.code[ls_num] = (YIELD_VALUE, None)
            code.code[ls_num + 1] = (STORE_FAST, lo_line[1])
            for num, line in enumerate(code.code):
                if line == lo_line:
                    if num >= ls_num:
                        code.code[num] = (LOAD_FAST, lo_line[1])
                    else:
                        pops.append(num)
    for num, line in enumerate(pops):
        code.code.pop(line - num)
    fnc.func_code = code.to_code()
    return fnc


def fastgen(fnc):
    return partial(gen.Task, fnc)

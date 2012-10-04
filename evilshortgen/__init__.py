from byteplay import (
    Code, STORE_FAST, YIELD_VALUE,
    BINARY_LSHIFT, SetLineno, LOAD_FAST,
    UNPACK_SEQUENCE,
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
    vars_count = 0
    last = []
    for num, line in enumerate(code.code):
        if SetLineno in line:
            if '<<' in source[line_num]:
                last = []
                vars_count = len(map(str.strip, 
                    source[line_num].split('<<')[0].split(','),
                ))
            line_num += 1
        elif vars_count:
            last.append((num, line))
            vars_count -= 1
        if BINARY_LSHIFT in line:
            code.code[num] = (YIELD_VALUE, None)
            increaser = 2
            if len(last) > 1:
                code.code.insert(num + 3, (UNPACK_SEQUENCE, len(last)))
                pops.append(num + 2)
                increaser = 4
            for store_num, store_line in enumerate(last):
                code.code.insert(num + increaser + store_num,
                    (STORE_FAST, store_line[1][1]))
            pops.append(num + 1)
            for _num, _line in enumerate(code.code):
                for store_line in last:
                    if _line == store_line[1]:
                        if _num >= num:
                            code.code[_num] = (LOAD_FAST, store_line[1][1])
                        else:
                            pops.append(_num)
    for num, line in enumerate(sorted(pops)):
        code.code.pop(line - num)
    fnc.func_code = code.to_code()
    return fnc


def fastgen(fnc):
    return partial(gen.Task, fnc)

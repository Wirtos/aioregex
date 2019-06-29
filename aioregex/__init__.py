import re, asyncio
from typing import Union, AnyStr
from inspect import iscoroutinefunction

REPATTERN_TYPE = type(re.compile(''))
REFLAGS_TYPE = type(re.I)


async def _lookahead(iterable):
    # looks for objects remained after iterated one to emulate ''.join() behaviour

    it = iter(iterable)
    try:
        last = next(it)
    except StopIteration:
        return
    for val in it:
        yield last, True
        last = val
    yield last, False


async def aiosub(pattern: Union[str, REPATTERN_TYPE],
                 repl: Union[str, callable, asyncio.coroutine],
                 string: str,
                 count: int = 0,
                 flags: REFLAGS_TYPE = 0):
    temp = []
    last_end = 0
    loookahead_matches = _lookahead(
        pattern.finditer(string) if isinstance(pattern, REPATTERN_TYPE)
        else re.finditer(pattern, string, flags=flags))

    async for match, items_left in loookahead_matches:
        if not count < 1 and len(temp) > count:
            temp.append(match.string[last_end:])
            await loookahead_matches.aclose()
            break

        temp.append(string[last_end:match.start()])

        if iscoroutinefunction(repl):
            temp.append(await repl(match))
        elif callable(repl):
            temp.append(repl(match))
        else:
            temp.append(match.expand(repl))
        if not items_left:
            temp.append(match.string[match.end():])
        last_end = match.end()
    return ''.join(temp) if temp else string


async def aiosubn(pattern: Union[str, REPATTERN_TYPE],
                  repl: Union[str, callable, asyncio.coroutine],
                  string: str,
                  count: int = 0,
                  flags: REFLAGS_TYPE = 0):
    temp = []
    last_end = 0
    repl_counter = 0
    loookahead_matches = _lookahead(
        pattern.finditer(string) if isinstance(pattern, REPATTERN_TYPE)
        else re.finditer(pattern, string, flags=flags))

    async for match, items_left in loookahead_matches:
        if not count < 1 and len(temp) > count:
            temp.append(match.string[last_end:])
            await loookahead_matches.aclose()
            break

        temp.append(string[last_end:match.start()])

        if iscoroutinefunction(repl):
            temp.append(await repl(match))
        elif callable(repl):
            temp.append(repl(match))
        else:
            temp.append(match.expand(repl))
        repl_counter += 1
        if not items_left:
            temp.append(match.string[match.end():])
        last_end = match.end()
    return ''.join(temp) if temp else string, repl_counter

"""Facilitates conversion of a nutshell file into a Golly-compatible .rule file."""
import os
import sys
from inspect import cleandoc

from ergo.misc import ErgoNamespace

from nutshell import segmentor, compiler, tools
from nutshell.common.utils import printq
from nutshell.cli import cli


def transpile(fp, *, preview=False, find=None):
    """
    Parses and compiles the given nutshell file into an equivalent .rule.
    """
    printq('\nParsing...')
    parsed = segmentor.parse(fp)
    if preview:
        tbl = parsed['@TABLE']
        return '{}\n\n{}'.format('\n'.join(f'{k}: {v}' for k, v in tbl.vars.items()), '\n'.join(', '.join(map(str, tr)) for tr in tbl))
    if find:
        print(parsed['@TABLE'].match(find) + '\n')
        return
    printq('Complete!', 'Compiling...', sep='\n\n')
    return compiler.compile(parsed)


def _preview(args):
    mock = f'''
      @TABLE
      states: {args.states}
      symmetries: {args.symmetries}
      neighborhood: {args.neighborhood}
      {args.transition}
    '''
    parsed = transpile(cleandoc(mock).splitlines(), preview=True)
    yield ('Complete! Transpiled preview:\n', parsed, '')


def _transpile(args):
    for infile in args.infiles:
        if infile == '-':
            finished = transpile(sys.stdin.read().splitlines(True), find=args.find)
        else:
            with open(infile) as infp:
                finished = transpile(infp, find=args.find)
        fname = os.path.split(infile)[-1].split('.')[0]
        for directory in args._.get('outdirs', ()):
            if directory == '-':
                yield finished.splitlines()
                continue
            with open(f'{os.path.join(directory, fname)}.rule', 'w') as outfp:
                outfp.write(finished)
                yield ('Complete!', '', f'Created {os.path.realpath(outfp.name)}')


def write_rule(**kwargs):
    for _ in _transpile(ErgoNamespace(**kwargs)):
        pass


def main():
    cli.prepare(strict=True, propagate_unknowns=True)
    inp = cli.result
    if inp is None:
        return
    if 'transpile' in inp:
        res = _transpile(inp.transpile)
    elif 'preview' in inp:
        res = _preview(inp.preview)
    elif 'icon' in inp:
        res = tools.dispatch(inp.icon)
    for val in res:
        printq(*val, sep='\n')

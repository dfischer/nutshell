from joffrey import CLI, Group

from nutshell import __version__

DEFAULT_HEADER = f'''\
********************************
**** COMPILED FROM NUTSHELL ****
**** {'v'+__version__: ^22} ****
********************************\
'''

cli = CLI("A transpiler from the 'Nutshell' rule-table format to Golly's")

transpile = cli.command(
  'transpile', 'Transpile from Nutshell to Golly ruletable format',
  aliases=['t'], OR='not nothing'
  )
transpile.main_grp = Group(XOR='find|normal')

icon = cli.command(
  'icon',
  'Tools related to the @ICONS section',
  aliases=['i'], OR='not nothing'
)


@cli.flag(short='V')
def version():
    raise SystemExit(__version__)


@cli.clump(XOR='verbose|quiet')
@cli.flag('verbosity', namespace={'count': 0}, default=0)
def verbose(nsp):
    """Repeat for more verbosity; max x4"""
    if nsp.count < 4:
        nsp.count += 1
    return nsp.count


@cli.clump(XOR='verbose|quiet')
@cli.flag(default=True)  # when imported as module. When run from console (as set in main.py), default=False
def quiet():
    return True


@transpile.main_grp.clump(AND='infiles|outdirs')
@transpile.arg()
def infiles(path: str.split):
    """
    Nutshell-formatted input file(s)
    Separate different files with a space, and use - (no more than once) for stdin.
    If you have a file in the current directory named -, use ./- instead.
    """
    if '-' in path:
        hyphen_idx = 1 + path.index('-')
        return path[:hyphen_idx] + [i for i in path[hyphen_idx:] if i != '-']
    return path


@transpile.clump(OR='find|outdirs', XOR='find|outdirs')
@transpile.main_grp.clump(AND='infiles|outdirs')
@transpile.main_grp.arg()
def outdirs(path: str.split):
    """
    Directory/ies to create output file in
    Separate dirnames with a space, and use - (no more than once) for stdout.
    If you have a directory under the current one named -, use -/ instead.
    """
    if '-' in path:
        hyphen_idx = 1 + path.index('-')
        return path[:hyphen_idx] + [i for i in path[hyphen_idx:] if i != '-']
    return path


@transpile.main_grp.flag(short='t', default=DEFAULT_HEADER)
def header(text=''):
    """Change or hide 'COMPILED FROM NUTSHELL' header"""
    return text


@transpile.main_grp.flag(short='s', aliases=['source'], default=None)
def comment_src(format_string='#### line {line}: {span} ####'):
    """
    Comment each Nutshell @TABLE line above the Golly line(s) it transpiles to
    
    Argument is a Python-style format string which, if given, will be treated as:
        yourstring.format(line=<LINE NUMBER>, span=<SPECIFIC TEXT FROM ORIGINAL LINE>)
    ...and then used to format the source-comment output.
    
    It should start with a # symbol to be treated as a comment by Golly. Default is '#### line {line}: {span} ####'.
    """
    return format_string


@transpile.main_grp.flag(short='c', aliases=['comments'], default=False)
def preserve_comments():
    """Transfer original Nutshell @TABLE comments into Golly output"""
    return True


@transpile.clump(OR='find|outdirs', XOR='find|outdirs')
@transpile.flag(short='f', default=None)
def find(transition):
    """Locate first transition in `infile` that matches"""
    return tuple(s if s in '*?' else int(s) for s in map(str.strip, transition.split(',')))

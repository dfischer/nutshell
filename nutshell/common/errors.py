"""Errors to be raised during nutshell parsing."""
class NutshellException(SystemExit):
    def __init__(self, lno: int, msg: str, seg_name: str = None, segment: list = None, shift: int = 0):
        """
        lno: line number error occurred on
        msg: error message
        seg: segment of rulefile error occurred in
        shift: line number seg starts on
        """
        start = f'\n  {self.__class__.__name__}' if seg_name is None else f'\n  {self.__class__.__name__} in {seg_name}'
        self.lno, self.span, self.msg = lno, None, msg
        if isinstance(lno, tuple):
            self.lno, *self.span = lno
        if isinstance(segment, list):
            code = [
              f'{start}, line {shift+self.lno}:',
              f'      {segment[self.lno-1]}'
              ]
            if self.span is not None:
                begin, end = self.span
                code.append(f"      {' ' * (begin - 1)}{'^' * (end - begin)}")
            code.append(f'  {msg}')
        else:
            code = [
              f'{start}:' if self.lno is None else f'{start}, line {shift+self.lno}:',
              f'      {msg}\n'
              ]
        self.lno = lno
        self.code = '\n'.join(code) + '\n'


class ReferenceErr(NutshellException):
    pass


class SyntaxErr(NutshellException):
    pass


class ValueErr(NutshellException):
    pass


class UnsupportedFeature(NutshellException):
    pass


class CoordOutOfBounds(ValueErr):
    pass
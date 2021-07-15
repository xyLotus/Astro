"""
The parser.
"""
from astro_types import TokenType
from typing import List, Callable
import sys
import avm
import re

__author__  = 'bellrise'
__version__ = '0.1'

if sys.version_info.minor < 5:
    raise RuntimeError('requires Python >= 3.5')


class Parser:
    """The parser takes a list of tokens that are the result from the
    tokenizer class, and returns a syntax tree that can then be turned into
    bytecode. In between parsing, different parts of the code are checked
    for invalid or useless code. This class can print an error telling you
    where the invalid code is located, and exit the program if the code
    cannot compile properly. """

    possible_checks = []

    signatures = (
        # ! name ( ... ) :
        (avm.BCO_FUNCTION, (
            TokenType.EXCL, TokenType.NAME, TokenType.LPAREN, ...,
            TokenType.RPAREN, TokenType.COLON)),
        # name ( ... )
        (avm.BCO_CALL, (
            TokenType.NAME, TokenType.LPAREN, ...,
            TokenType.RPAREN)),
        # name ...
        (avm.BCO_BASECALL, (TokenType.NAME, ...)),
        # name = ...
        (avm.BCO_ASSIGN, (TokenType.NAME, TokenType.ASSIGN, ...))
    )

    def __init__(self, filename: str, tokens: List[dict], trust_me=False):
        """Setup the parser instance. This takes a token list. To actually
        start the parsing process, call parse() on the created object.
        :param filename: path to the file currently being compiled
        :param tokens:   list of context groups
        :param trust_me: True if the parser should trust the developer with
                         the data format
        """
        self.filename = filename
        self.tokens = tokens
        self.checks = []

        # This is set in trap_errors
        self.error_callback = None

        if not trust_me:
            if not isinstance(tokens[0], dict):
                raise TypeError('token context should be a dict')

            required_fields = 'line', 'source', 'tokens'
            for token in tokens:
                if not all(key in token for key in required_fields):
                    raise KeyError('missing keys in token context')

    def parse(self, checks=...) -> list:
        """Start parsing the provided token list, turning it into a syntax
        tree that can then be synthesized into bytecode.
        :param checks: a list of checks the parser should run, by default
                       all checks are enabled
        """
        if checks is ...:
            self.checks = self.possible_checks

        for token_ctx in self.tokens:
            tokens = token_ctx['tokens']
            result = self.match(tokens)
            if not result:
                self.error(token_ctx, 'invalid syntax')

        return []

    def match(self, tokens: List[TokenType]) -> int:
        """Match a token list to a statement type, and then return that tuple
        of the type and function to call to parse it.
        :param tokens: list of token types
        """
        for _sig in self.signatures:
            # Check each signature for a matching one
            id_, sig = _sig
            tok_index = 0
            for sig_index, element in enumerate(sig):
                # If the element in the signature is an ellipsis, skip until it
                # finds the next element in the token list or to the end if no
                # element is found after the ellipsis.
                if element is ...:
                    if sig_index - 1 == len(sig):
                        return id_
                    if sig[sig_index+1] is ...:
                        raise SyntaxError('there cannot be 2 ellipsis in a sig')

                    pos = tokens[tok_index:].index(sig[sig_index+1])
                    if pos == -1:
                        # If the next token hasn't been found, skip to another
                        # signature.
                        break

                    # We have to take in account that we're taking a slice of
                    # the tokens list
                    tok_index += pos
                    continue

                if not element == tokens[tok_index]:
                    break

                tok_index += 1

            # We found a match!
            if tok_index == len(tokens):
                return id_

        return 0

    def trap_errors(self, callback: Callable[[str, dict], None]):
        """Catch any errors that could close the parser, passing the error
        message and the token context to the function.
        :param callback: a function that will be called when an error occurs.
        """
        self.error_callback = callback

    def error(self, ctx: dict, *msg, at=0, size=0, sep=' '):
        """Print a compilation error and exit.
        :param ctx: line context - index, filename and source
        :param msg: any amount of data to print after that
        :param at: index at where the error happened
        :param size: length of the squiggly
        :param sep: separator, default is space
        """
        if self.error_callback:
            self.error_callback(msg, ctx)
            return
        self._print_problem('Compilation error', ctx, *msg, at=at,
                            size=size, sep=sep)
        exit(1)

    def warn(self, ctx: dict, *msg, at=0, size=0, sep=' '):
        """Print a warning.
        :param ctx: line context - index, filename and source
        :param msg: any amount of data to print after that
        :param at: index at where the error happened
        :param size: length of the squiggly
        :param sep: separator, default is space
        """
        self._print_problem('Compilation warning', ctx, *msg, at=at,
                            size=size, sep=sep)

    def _print_problem(self, title, ctx, *msg, at, size, sep):
        """Print an error/warning from error() or warn(). """

        msg = sep.join([str(x) for x in msg])
        if not size:
            size = len(ctx['source'])
        if self.error_callback:
            self.error_callback(msg, ctx)
            return

        # We want to skip whitespace for the squiggly
        match = re.match(r'^\s*', ctx['source'])
        if match:
            offset = match.span()[1]
            size -= offset
            at += offset

        print(
            f'{title} in {self.filename}:\n',
            f'{ctx["line"]:4} | {ctx["source"]}\n',
            ' ' * 7, ' ' * at, '^' + '~' * (size - 1), '\n',
            msg, sep='', file=sys.stderr
        )


if __name__ == '__main__':
    # This is a small piece of code for testing the general functionality
    # of the parser, real unit tests will be written.
    __parser = Parser('test.asx', [
        {'line': 1, 'source': '! function(param, param2):', 'tokens': [
            TokenType.EXCL, TokenType.NAME, TokenType.LPAREN, TokenType.NAME,
            TokenType.COMMA, TokenType.NAME, TokenType.RPAREN, TokenType.COLON
        ]},
        {'line': 2, 'source': '    out param', 'tokens': [
            TokenType.TAB, TokenType.NAME, TokenType.NAME
        ]}
    ])

    if __parser.parse() != [
        {
            'type': avm.BCO_FUNCTION,
            'name': 'function',
            'params': ['param', 'param2'],
            'code': [
                {'type': avm.BCO_BASECALL, 'call': 'out', 'params': [
                    {'type': 'var', 'name': 'param'}
                ]}
            ]
        }
    ]:
        print('failed to parse')

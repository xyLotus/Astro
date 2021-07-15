""" The file where the definition of the Tokenizer
class is stored. """

from astro_types import Token, TokenType
from astro_file import AstroFile

__author__  = 'xyLotus'
__version__ = '0.1.0'   # sub-release [10% finished]


class Tokenizer:
    """ This class tokenizes the given files
    given in @member h_file and returns the tokens
    per line uncompressed and raw. """

    def __init__(self, h_file: AstroFile):
        """ @member file = file to be tokenized,
        @member tokens, token list; used in @method tokenize. """
        self.is_compressed = False
        self.h_file = h_file
        self.tokens = []
        self.content = self.h_file.content

    def output_tokens(self):
        """ Outputs tokens in human easy-to-read format
        for debugging and readability purposes """
        for line in self.tokens:
            for tok in line:
                print(tok, end=' ')
            print()

    def get_context(self):
        """ Returns context in dict format providing
        line, source and tokens. Should probably only
        be called when tokens are compressed. """
        if not self.is_compressed:
            print(f'[Tokenizer-Error]: Compress tokens with compress();')
            exit(1)

        context_list = []
        sources = self.content.split('\n')
        for i, line in enumerate(self.tokens):
            context_list.append({
                'line': i + 1,
                'source': sources[i],
                'tokens': self.tokens[i]
            })

        return context_list

    def tokenize(self) -> list:
        """ Tokenizes given file by accessing file handle
        @member h_file (AstroFile) and storing the tokens in @member tokens."""
        toks = []

        type_map = {
            ' ': TokenType.SPACE,
            '!': TokenType.EXCL,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            ':': TokenType.COLON,
            ',': TokenType.COMMA
        }

        for line in self.content.split('\n'):
            line_buffer = []
            for ch in line:
                typ = type_map.get(ch, TokenType.SYM)
                line_buffer.append(Token(typ, ch))
            toks.append(line_buffer)

        # Compress all required tokens
        toks = self.compress(toks, TokenType.SYM, TokenType.NAME)

        self.tokens = toks
        return toks

    def compress(self, tokens: list, from_: int, to_: int) -> list:
        """ Compresses the tokens into sub-tokens which
        are smaller, ready for compilation and syntax lexing,
        overwriting @member self.compressed_tokens. """
        self.is_compressed = True

        # compress token sets line by line
        toks = []
        for line in tokens:
            value_buf = ""
            line_buf = []

            # line compression process
            for i, tok in enumerate(line):
                if tok.id != from_:
                    line_buf.append(tok)

                if i != len(line) - 1:  # End Of Token Set!
                    if tok.id == from_ and line[i+1].id == from_:
                        value_buf += tok.value
                    elif tok.id == from_ and line[i+1].id != from_:
                        value_buf += tok.value

                        line_buf.append(Token(id_=to_, value=value_buf))
                        value_buf = ""
                elif tok.id == from_:
                    value_buf += tok.value
                    
                    line_buf.append(Token(id_=to_, value=value_buf))
                    value_buf = ""  # clear buffer

            toks.append(line_buf)

        return toks

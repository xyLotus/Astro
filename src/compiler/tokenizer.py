""" The file where the definition of the Tokenizer
class is stored. """

from astro_file import AstroFile
from astro_types import Token, TokenType

__author__ = 'xyLotus'
__version__ = '0.1.0' # sub-release [10% finished]

class Tokenizer:
    """ This class tokenizes the given files
    given in @member h_file and returns the tokens
    per line uncompressed and raw. """

    def __init__(self, h_file: AstroFile):
        """ @member file = file to be tokenized,
        @member tokens, token list; used in @method tokenize. """
        self.h_file = h_file
        self.tokens = []

        with open(h_file.file_name, 'r') as f:
            self.content = f.read()

    def output_tokens(self):
        """ Outputs tokens in human easy-to-read format
        for debugging and readability purposes """
        for line in self.tokens:
            print('__[NEWLINE]__')
            for tok in line:
                print(tok, end=' ')

    def tokenize(self):
        """ Tokenizes given file by accessing file handle
        @member h_file (AstroFile) and storing the tokens in @member tokens."""
        line_buffer = []

        for line in self.content.split('\n'):
            line_buffer = []
            for ch in line:
                if   ch == ' ':
                    line_buffer.append(Token(TokenType.SPACE,  ch))
                elif ch == '!':
                    line_buffer.append(Token(TokenType.EXCL,   ch))
                elif ch == '(':
                    line_buffer.append(Token(TokenType.LPAREN, ch))
                elif ch == ')':
                    line_buffer.append(Token(TokenType.RPAREN, ch))
                elif ch == ':':
                    line_buffer.append(Token(TokenType.COLON,  ch))
                elif ch == ',':
                    line_buffer.append(Token(TokenType.COMMA,  ch))
                else:
                    line_buffer.append(Token(TokenType.SYM,    ch))
            self.tokens.append(line_buffer)

    def compress(self, token_id: int):
        """ Compresses the tokens into sub-tokens which
        are smaller, ready for compilation and syntaxlexing,
        accesses @member self.compressed_tokens. """
        
        # compress token sets line by line
        toks = []
        for line in self.tokens:
            value_buf = ""
            line_buf = []

            # line compression process
            for i, tok in enumerate(line):
                if tok.id != token_id:
                    line_buf.append(tok)

                if i != len(line)-1: # End Of Token Set!
                    if tok.id == token_id and line[i+1].id == token_id:
                        value_buf += tok.value
                    elif tok.id == token_id and line[i+1].id != token_id:
                        value_buf += tok.value

                        line_buf.append(Token(id_ = 13, value = value_buf))
                        value_buf = ""
                elif tok.id == token_id:
                    value_buf += tok.value
                    
                    line_buf.append(Token(id_ = 13, value = value_buf))
                    value_buf = "" # clear buffer

            toks.append(line_buf)

        for line in toks:
            print()
            for tok in line:
                print(tok, end = '')

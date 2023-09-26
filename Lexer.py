from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Square brackets
        self.lexer.add('LSB',r'\[\s*')
        self.lexer.add('RSB',r'\s*\]')
        # Vertical bar
        self.lexer.add('VB',r'\s*\|\s*')
        # Equals sign
        self.lexer.add('EQ',r'\s*=\s*')
        # Any character string (maybe)
        self.lexer.add('STR',r'[^\[\]\|=]+') # token, digital, new line and space maybe not treat as MSTR

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
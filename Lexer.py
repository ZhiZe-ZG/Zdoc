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
        # Any character string (except [ | = ] \s)
        # not end with \s, but can be \s sequence before '[' and after ']'
        self.lexer.add('STR',r'([^\[\]\|=]*[^\[\]\|=\s])|\s+') 

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
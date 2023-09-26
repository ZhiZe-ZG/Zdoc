from Lexer import Lexer
from Parser import Parser

text_input = """
print(4 + 4 - 2);
"""

path = "./test/test.zdoc"
outpath = "./test/test.zdox"

with open(path, "r", encoding="utf-8") as f:
    content = "".join(f.readlines())

# text_input = content

# lexer = Lexer().get_lexer()
# tokens = lexer.lex(text_input)

# for token in tokens:
#     print(token)

""""""

text_input = """
print(4 + 4 - 2);
"""

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

pg = Parser()
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()

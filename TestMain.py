from Lexer import Lexer
from Parser import Parser
from MarkdownGenerator import generate_markdown

path = "./test/test.zdoc"
outpath = "./test/test.md"

with open(path, "r", encoding="utf-8") as f:
    content = "".join(f.readlines())

lexer = Lexer().get_lexer()
tokens = lexer.lex(content)

for token in tokens:
    print(token)

tokens = lexer.lex(content)
pg = Parser()
pg.parse()
parser = pg.get_parser()
# print(parser.lr_table.default_reductions[0])
# print(parser.lr_table)
output = parser.parse(tokens)

print(output)
print(output.list)
print(output.list[0].name)
print(output.list[0].attribute)
print(output.list[0].value)

md = generate_markdown(output)
print('Markdown')
print(md)
# print(next(tokens))

with open(outpath, "w", encoding="utf-8") as f:
    f.write(md)
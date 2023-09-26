from Lexer import Lexer
from Parser import Parser

text_input = """[zdoc|
font=Arial|
size=24|
[h|Zdoc 标准说明]
这是一个 zdoc 的[b|文档]，用于说明 [i|zdoc] 的使用方法。
此外还有换行和[blue|  空白  ][red|字符]的问题。

[math|
y [eq] ax^2 + bx + c
]

这是一个特殊的[spacial|
https://www.abc.xyz
{
    fun{

    }
}
]
]"""

path = "./test/test.zdoc"
outpath = "./test/test.zdox"

with open(path, "r", encoding="utf-8") as f:
    content = "".join(f.readlines())

# text_input = """[hello]"""
lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

# for token in tokens:
#     print(token)

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

# print(next(tokens))
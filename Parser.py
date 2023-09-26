from rply import ParserGenerator
from AST import Attribute, AttributeList, TagStringList, Tag


class Parser:
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ["LSB", "RSB", "VB", "EQ", "STR"]
        )

    def get_parser(self):
        return self.pg.build()

    def parse(self):
        @self.pg.production("tagstringlist : STR")
        def tagstringlist_head_str(p):
            return TagStringList([p[0].value])

        @self.pg.production("tagstringlist : tag")
        def tagstringlist_head_tag(p):
            return TagStringList([p[0]])

        @self.pg.production("tagstringlist : tagstringlist STR")
        def tagstringlist_str(p):
            return TagStringList(p[0].list + [p[1].value])

        @self.pg.production("tagstringlist : tagstringlist tag")
        def tagstringlist_tag(p):
            return TagStringList(p[0].list + [p[1]])

        @self.pg.production("tag : LSB STR RSB")
        def tag1(p):
            return Tag(p[1].value, [], [])

        @self.pg.production("tag : LSB STR VB attributelist RSB")
        def tag21(p):
            return Tag(p[1].value, p[3].list, [])

        @self.pg.production("tag : LSB STR VB tagstringlist RSB")
        def tag22(p):
            return Tag(p[1].value, [], p[3].list)

        @self.pg.production("tag : LSB STR VB attributelist VB tagstringlist RSB")
        def tag3(p):
            return Tag(p[1].value, p[3].list, p[5].list)

        @self.pg.production("attribute : STR EQ tagstringlist ")
        def attribute(p):
            return Attribute(p[0].value, p[2].list)

        @self.pg.production("attributelist : attribute ")
        def attributelist_head(p):
            return AttributeList([p[0]])

        @self.pg.production("attributelist : attributelist VB attribute ")
        def attributelist(p):
            return AttributeList(p[0].list + [p[2]])

        @self.pg.error
        def error_handle(token):
            raise ValueError(
                "Ran into a %s where it wasn't expected" % token.gettokentype()
            )

from rply.token import BaseBox

class Attribute(BaseBox):
    def __init__(self, name,value):
        self.name = name
        self.value = value

    def eval(self):
        return self.value
    
class AttributeList(BaseBox):
    def __init__(self, list):
        self.list = list

    def eval(self):
        return self.list
    
class Tag(BaseBox):
    def __init__(self, name,attribute,value):
        self.name = name
        self.attribute  = attribute
        self.value = value

    def eval(self):
        return self.value
    
class TagStringList(BaseBox):
    def __init__(self, list):
        self.list = list

    def eval(self):
        return self.list

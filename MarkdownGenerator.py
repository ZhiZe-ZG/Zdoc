# from AST import Attribute, AttributeList, Tag, TagStringList
import AST
def generate_markdown(tree):
    L = []
    run_next = True
    if type(tree).__name__ == 'TagStringList':
        LL = tree.list
    else:
        LL = [tree]
    while run_next:
        for item in LL:
            if type(item).__name__ == 'str':
                L.append(item)
            elif type(item).__name__ == 'Tag':
                L = L + handle_Tag(item)
        
        run_next = False
        for item in L:
            if not(type(item).__name__ == 'str'):
                run_next = True
        print('--------------')
        if run_next:
            LL = L
            L = []

    return ''.join(L)

def handle_Tag(x):
    if x.name == 'zdoc':
        L = x.value
    elif x.name == 'i':
        L = ['*'] + x.value + ['*']
    elif x.name == 'b':
        L = ['**'] + x.value + ['**']
    elif x.name == 'h':
        L = ['# '] + x.value
    elif x.name == 'math':
        L = ['$$'] + x.value + ['$$']
    elif x.name == 'eq':
        L = ['=']
    elif x.name == 'rsb':
        L = [']']
    elif x.name == 'lsb':
        L = ['[']
    elif x.name == 'vb':
        L = ['|']
    elif x.name == 'lf':
        L = ['\n']
    elif x.name == 'sp':
        L = [' ']
    elif x.name == 'code':
        lan = ''
        for attr in x.attribute:
            if attr.name == 'language':
                lan = attr.value[0]
        L = [f'```{lan}\n'] + x.value + ['\n```\n']
    elif x.name == 'url':
        L = ['<'] + x.value + ['>']
    else:
        # print(x.name)
        L = [f'[{x.name}']
        for attr in x.attribute:
            L.append(f'|{attr.name}=')
            L = L+attr.value
        if len(x.value) > 0:
            L = L + ['|']
            L = L + x.value
        L = L + [']']
    return L

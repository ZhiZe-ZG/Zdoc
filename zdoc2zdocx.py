from typing import List, Union, Self,Pattern, Tuple

import re
# from functools import cached_property

# import sys
# sys.setrecursionlimit(100000)

path = './test/test.zdoc'
outpath = './test/test.zdox'

class ZLabel:
    def __init__(self, name:str, children:Union[None,List[Self], str]):
        self.name = name
        self.children = children

class EndLineZLabel(ZLabel):
    def __init__(self):
        self.name = 'EndLine'
        self.children = None

def parse_minimal_ZLabel(x:str)->ZLabel:
    """
    x should be a minimal ZLabel
    """
    sp = x.split('|')
    name = sp[0].replace('[','')
    children = sp[1].replace(']', '')
    return ZLabel(name, children)

minimal_zlabel_re = re.compile(r'\[[\.\w]*\|[^\[\]]*\]')
test_re = re.compile(r'10')

def split_minimal_zlabel(x:str)->Tuple[List[str], List[str]]:
    # split
    other_content = minimal_zlabel_re.split(x)
    minimal_zlabel = [x[p.start():p.end()] for p in minimal_zlabel_re.finditer(x)]
    return other_content,minimal_zlabel

LeftSymbol = '<==='
RightSymbol ='===>'

final_re = re.compile(r'')
compiler_symbol_re = re.compile(r'<===\d+===>')

def split_compiler_symbol(x:str)->Tuple[List[str], List[str]]:
    # split
    other_content = compiler_symbol_re.split(x)
    minimal_zlabel = [x[p.start():p.end()] for p in compiler_symbol_re.finditer(x)]
    return other_content,minimal_zlabel

def check_children(x:ZLabel)->bool:
    if x.children is None:
        return False
    elif type(x.children) is list:
        return False
    elif type(x.children) is str:
        if len([ii for ii in compiler_symbol_re.finditer(x.children)])>0:
            return True
        else:
            return False
    else:
        return False
    
def check_expandable(x:str)->bool:
    return len([ii for ii in compiler_symbol_re.finditer(x)])>0

def check_is_minimal_expand(x:Union[ZLabel, str])->bool:
    if type(x) is str:
        return True
    elif x.children is None:
        return True
    elif type(x.children) is str:
        return True
    else:
        return False

def expand_ZLabel_List(ZL:List[ZLabel])->str:
    while any([(not (type(z) is str)) for z in ZL]):
        new_list = []
        for z in ZL:
            if type(z) is str:
                new_list.append(z)
            elif z.children is None:
                new_list.append(f'[{z.name}|]')
            elif type(z.children) is str:
                new_list.append(f'[{z.name}|{z.children}]')
            else:
                new_list.append(f'[{z.name}|')
                new_list = new_list+z.children
                print(z.children)
                new_list.append(']')
        ZL = new_list
        # print(ZL)
    return ''.join(ZL)

def expand_ZLabel(x:ZLabel)->str:
    if x.children is None:
        return f'[{x.name}|]'
    elif type(x.children) is list:
        return ''.join([expand_ZLabel(z) for z in x.children])
    else:
        return f'[{x.name}|{x.children}]'
        

def detect_str(x:str)->List[ZLabel]:
    ZL=[]
    ZL_origin = []
    while True:
        # split
        other_content, minimal_zlabel = split_minimal_zlabel(x)
        # parse minimal ZLabels
        Zlabels = [parse_minimal_ZLabel(m) for m in minimal_zlabel]
        # replace and add to list
        replace_str = [LeftSymbol+f'{idx+len(ZL)}'+RightSymbol for idx,m in enumerate(minimal_zlabel)]
        ZL = ZL+Zlabels
        ZL_origin = ZL_origin + minimal_zlabel
        # join str
        replace_str.append('') 
        pack = zip(other_content, replace_str) 
        pack = [p[0]+p[1] for p in pack]
        x =  ''.join(pack)
        if len([p for p in minimal_zlabel_re.finditer(x)])<=0:
            # print('final', x)
            break
    # handle final x
    # split
    other_content, compiler_symbols = split_compiler_symbol(x)
    compiler_symbols = [int(c.replace(LeftSymbol, '').replace(RightSymbol, '')) for c in compiler_symbols]
    merge_List = []
    for i in range(len(compiler_symbols)):
        if not other_content[i] == '':
            merge_List.append(ZLabel('text',other_content[i]))
        merge_List.append(ZL[compiler_symbols[i]])
    out_list = merge_List
    C_list = merge_List
    # handle all list
    goon = any([check_children(c) for c in C_list])
    while goon:
        new_list = []
        for c in C_list:
            if check_children(c):
                # split
                other_content, compiler_symbols = split_compiler_symbol(c.children)
                compiler_symbols = [int(cc.replace(LeftSymbol, '').replace(RightSymbol, '')) for cc in compiler_symbols]
                merge_List = []
                for i in range(len(compiler_symbols)):
                    if not other_content[i] == '':
                        merge_List.append(ZLabel('text',other_content[i]))
                    merge_List.append(ZL[compiler_symbols[i]])
                # append last one
                if not other_content[-1]=='':
                    merge_List.append(ZLabel('text',other_content[-1]))
                c.children = merge_List
                new_list = new_list+c.children
        C_list = new_list
        goon = any([check_children(c) for c in C_list])
    print('----')

    return out_list

def uniform_line_breaks(x:str)->str:
    x = x.replace('\r\n', '\n')
    x = x.replace('\r', '\n')
    return x

head_lf = re.compile(r'\[[\.\w]*\|\n')
tail_lf = re.compile(r'\n?\]')

def remove_lf_in_pattern(x:str, pt:Pattern[str]):
    """
    remove line feed in pattern matches
    """
    # split
    other_content = pt.split(x)
    with_lf = [x[p.start():p.end()] for p in pt.finditer(x)]
    # remove lf
    with_lf = [s.replace('\n','') for s in with_lf] # remove \n
    with_lf.append('') # len(other_content)=len(with_lf)+1
    pack = zip(other_content, with_lf) # other_content before with_lf
    pack = [p[0]+p[1] for p in pack]
    return ''.join(pack)

def remove_typesetting_lf(x:str)->str:
    x = remove_lf_in_pattern(x, head_lf)
    x = remove_lf_in_pattern(x, tail_lf)
    return x

EndLineSymbol = '[el|]'

def replace_lf(x:str)->str:
    x = x.replace('\n', EndLineSymbol)
    return x

with open(path, 'r', encoding='utf-8') as f:
    content = ''.join(f.readlines())

# clean grammar sugars
pre_funcs = [uniform_line_breaks, remove_typesetting_lf, replace_lf]
for f in pre_funcs:
    content = f(content)

out_list = detect_str(content)

for o in out_list:
    if (type(o.children) is None) or (type(o.children) is str):
        print(o.name, o.children)
    elif type(o.children) is list:
        print(o.name)
        print('----children----')
        for oo in o.children:
            print(oo.name, oo.children)
        print('------------')

with open(outpath, 'w', encoding='utf-8') as f:
    f.write(content)

# show [br|]

content = content.replace(EndLineSymbol,EndLineSymbol+'\n')

with open(outpath+'.show', 'w', encoding='utf-8') as f:
    f.write(content)

recover = expand_ZLabel_List(out_list)

recover = recover.replace(EndLineSymbol,EndLineSymbol+'\n')

with open(outpath+'.rec', 'w', encoding='utf-8') as f:
    f.write(recover)
    f.write('-------')
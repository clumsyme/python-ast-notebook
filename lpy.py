#!/usr/bin/env python

from ast import *
import argparse
from time import gmtime, strftime

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('filename', metavar='filename', type=str, nargs=1, help='需要执行的文件名')

args = parser.parse_args()

filename = args.filename[0]


class Visitor(NodeVisitor):
    def visit_Num(self, node):
        print('visit Num', node.n)

class Transformer(NodeTransformer):
    def visit_Call(self, node):
        default_prefix = [Str(s=strftime("print at %a, %d %b %Y %H:%M:%S: --> ", gmtime()))]

        if type(node.func) == Name and node.func.id == 'print':
            return Call(
                func=node.func,
                args=default_prefix + node.args,
                keywords=node.keywords,
            )
        return node

    def visit_FunctionDef(self, node):
        self.generic_visit(node)

        if type(node.body[-1]) == Expr:
            return FunctionDef(
                name=node.name,
                args=node.args,
                decorator_list=node.decorator_list,
                returns=node.returns,
                body=node.body[:-1] + [Return(value=node.body[-1].value)],
            )
        return node


with open(filename, 'r') as f:
    source = f.read()
    ast = parse(source)
    print('-' * 20)
    Visitor().visit(ast)
    print('-' * 20)
    Transformer().visit(ast)
    fix_missing_locations(ast)
    code = compile(ast, '<>', 'exec')
    exec(code)

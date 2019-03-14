# -*- coding: utf-8 -*-
import random
from deap import gp
import operator


def loosely_typed_gp():
    pset = gp.PrimitiveSet('main', 2)
    pset.addPrimitive(max, 2)
    pset.addPrimitive(operator.add, 2)
    pset.addPrimitive(operator.mul, 2)
    pset.addTerminal(3)
    pset.renameArguments(ARG0='x')
    pset.renameArguments(ARG1='y')
    pset.renameArguments(ARG2='z')
    pset.addPrimitive(operator.neg, 1)

    expr = gp.genFull(pset, min_=1, max_=3)
    tree = gp.PrimitiveTree(expr)
    print expr
    print tree
    print gp.stringify(tree)
    function = gp.lambdify(tree, pset)
    print function(1, 2)

    pset.addEphemeralConstant(lambda: random.uniform(-1, 1))
    expr = gp.genFull(pset, min_=1, max_=3)
    print expr


def if_then_else(input, output1, output2):
    return output1 if input else output2


def strongly_typed_gp():
    pset = gp.PrimitiveSetTyped('main', [bool, float], float)
    pset.addPrimitive(operator.xor, [bool, bool], bool)
    pset.addPrimitive(operator.mul, [float, float], float)
    pset.addPrimitive(if_then_else, [bool, float, float], float)
    pset.addTerminal(3.0, float)
    pset.addTerminal(1, bool)
    pset.renameArguments(ARG0='x')
    pset.renameArguments(ARG1='y')

    expr = gp.genFull(pset, min_=1, max_=3, type_=float)
    tree = gp.PrimitiveTree(expr)
    print expr
    print tree
    print gp.stringify(tree)

    pset.addEphemeralConstant(lambda: random.randint(-10, 10), float)
    expr = gp.genFull(pset, min_=1, max_=3, type_=float)
    print expr


def main():
    loosely_typed_gp()


if __name__ == '__main__':
    main()

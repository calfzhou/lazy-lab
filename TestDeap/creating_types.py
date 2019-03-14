# -*- coding: utf-8 -*-
import random
import array
from deap import base, creator, tools, gp
import operator


def list_of_floats():
    creator.create('FitnessMax', base.Fitness, weights=(1.0,))
    creator.create('Individual', list, fitness=creator.FitnessMax)

    IND_SIZE = 10
    toolbox = base.Toolbox()
    toolbox.register('attr_float', random.random)
    toolbox.register('individual', tools.initRepeat, creator.Individual,
                     toolbox.attr_float, n=IND_SIZE)

    individual = toolbox.individual()
    print individual


def permutation():
    creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
    creator.create('Individual', list, fitness=creator.FitnessMin)

    IND_SIZE = 10
    toolbox = base.Toolbox()
    toolbox.register('indices', random.sample, range(IND_SIZE), IND_SIZE)
    toolbox.register('individual', tools.initIterate, creator.Individual,
                     toolbox.indices)

    individual = toolbox.individual()
    print individual


def arithmetic_expression():
    pset = gp.PrimitiveSet('MAIN', arity=1)
    pset.addPrimitive(operator.add, 2)
    pset.addPrimitive(operator.sub, 2)
    pset.addPrimitive(operator.mul, 2)
    pset.addPrimitive(operator.neg, 1)

    creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
    creator.create('Individual', gp.PrimitiveTree, fitness=creator.FitnessMin, pset=pset)

    toolbox = base.Toolbox()
    toolbox.register('expr', gp.genRamped, pset=pset, min_=1, max_=2)
    toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.expr)

    individual = toolbox.individual()
    print individual


def initES(icls, scls, size, imin, imax, smin, smax):
    ind = icls(random.uniform(imin, imax) for _ in xrange(size))
    ind.strategy = scls(random.uniform(smin, smax) for _ in xrange(size))
    return ind


def evolution_strategy():
    creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
    creator.create('Individual', array.array, typecode='d',
                   fitness=creator.FitnessMin, strategy=None)
    creator.create('Strategy', array.array, typecode='d')

    IND_SIZE = 5
    MIN_VALUE, MAX_VALUE = -5.0, 5.0
    MIN_STRAT, MAX_STRAT = -1.0, 1.0

    toolbox = base.Toolbox()
    toolbox.register('individual', initES, creator.Individual, creator.Strategy,
                     IND_SIZE, MIN_VALUE, MAX_VALUE, MIN_STRAT, MAX_STRAT)

    individual = toolbox.individual()
    print individual
    print individual.strategy


def initParticle(pcls, size, pmin, pmax, smin, smax):
    part = pcls(random.uniform(pmin, pmax) for _ in xrange(size))
    part.speed = [random.uniform(smin, smax) for _ in xrange(size)]
    part.smin = smin
    part.smax = smax
    return part


def particle():
    creator.create('FitnessMax', base.Fitness, weights=(1.0, 1.0))
    creator.create('Particle', list, fitness=creator.FitnessMax,
                   speed=None, smin=None, smax=None, best=None)

    toolbox = base.Toolbox()
    toolbox.register('particle', initParticle, creator.Particle,
                     size=2, pmin=-6, pmax=6, smin=-2, smax=3)

    p1 = toolbox.particle()
    p2 = toolbox.particle()
    print p1, p1.speed
    print p2, p2.speed


def funky_one():
    creator.create('FitnessMax', base.Fitness, weights=(1.0, 1.0))
    creator.create('Individual', list, fitness=creator.FitnessMax)

    INT_MIN, INT_MAX = 5, 10
    FLT_MIN, FLT_MAX = -0.2, 0.8
    N_CYCLES = 4

    toolbox = base.Toolbox()
    toolbox.register('attr_int', random.randint, INT_MIN, INT_MAX)
    toolbox.register('attr_flt', random.uniform, FLT_MIN, FLT_MAX)
    toolbox.register('individual', tools.initCycle, creator.Individual,
                     (toolbox.attr_int, toolbox.attr_flt), n=N_CYCLES)

    individual = toolbox.individual()
    print individual


def main():
    funky_one()


if __name__ == '__main__':
    main()

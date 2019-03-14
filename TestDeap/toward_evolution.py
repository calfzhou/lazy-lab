# -*- coding: utf-8 -*-
import random
from deap import base, creator, tools


def evaluate(individual):
    a = sum(individual)
    b = len(individual)
    return a, 1.0 / b


def main():
    # A first individual.
    print 'Individual:'
    IND_SIZE = 5

    creator.create('FitnessMin', base.Fitness, weights=(-1.0, -1.0))
    creator.create('Individual', list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register('attr_float', random.random)
    toolbox.register('individual', tools.initRepeat, creator.Individual,
                     toolbox.attr_float, n=IND_SIZE)

    ind1 = toolbox.individual()
    print ind1
    print ind1.fitness.valid

    # Evaluation.
    print 'Evaluation:'
    ind1.fitness.values = evaluate(ind1)
    print ind1.fitness.valid
    print ind1.fitness

    # Mutation.
    print 'Mutation:'
    mutant = toolbox.clone(ind1)
    ind2, = tools.mutGaussian(mutant, mu=0.0, sigma=0.2, indpb=0.2)
    del mutant.fitness.values

    print mutant is ind1
    print mutant is ind2
    print mutant

    # Crossover.
    print 'Crossover:'
    #ind2 = toolbox.individual()
    #print ind1
    #print ind2

    child1, child2 = [toolbox.clone(ind) for ind in (ind1, ind2)]
    tools.cxBlend(child1, child2, 0.5)
    del child1.fitness.values
    del child2.fitness.values

    print child1
    print child2

    # Selection.
    print 'Selection:'
    selected = tools.selBest([child1, child2], 2)
    print child1 in selected
    offspring = [toolbox.clone(ind) for ind in selected]

    # Using the toolbox.
    print 'Toolbox:'
    toolbox.register('mate', tools.cxTwoPoints)
    toolbox.register('mutate', tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
    toolbox.register('select', tools.selTournament, tournsize=3)
    toolbox.register('evaluate', evaluate)

    # Using the tools.
    print 'Tools:'


if __name__ == '__main__':
    main()

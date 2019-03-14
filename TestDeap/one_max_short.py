# -*- coding: utf-8 -*-
from deap import base, creator, tools, algorithms
import random


def eval_one_max(individual):
    return sum(individual),


def one_max():
    creator.create('FitnessMax', base.Fitness, weights=(1.0, ))
    creator.create('Individual', list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register('attr_bool', random.randint, 0, 1)
    toolbox.register('individual', tools.initRepeat, creator.Individual,
                     toolbox.attr_bool, 32)

    toolbox.register('population', tools.initRepeat, list, toolbox.individual)

    toolbox.register('evaluate', eval_one_max)
    toolbox.register('mate', tools.cxTwoPoints)
    toolbox.register('mutate', tools.mutFlipBit, indpb=0.05)
    toolbox.register('select', tools.selTournament, tournsize=3)

    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register('avg', tools.mean)
    stats.register('std', tools.std)
    stats.register('min', min)
    stats.register('max', max)

    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40,
                       stats=stats, halloffame=hof, verbose=True)


def main():
    one_max()


if __name__ == '__main__':
    main()

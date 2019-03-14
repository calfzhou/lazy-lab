# -*- coding: utf-8 -*-
import random
from deap import base, creator, tools


def eval_one_max(individual):
    return sum(individual),


def one_max():
    creator.create('FitnessMax', base.Fitness, weights=(1.0, ))
    creator.create('Individual', list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    # Attribute generator.
    toolbox.register('attr_bool', random.randint, 0, 1)
    # Structure initializers.
    toolbox.register('individual', tools.initRepeat, creator.Individual,
                     toolbox.attr_bool, 32)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)

    toolbox.register('evaluate', eval_one_max)
    toolbox.register('mate', tools.cxTwoPoints)
    toolbox.register('mutate', tools.mutFlipBit, indpb=0.05)
    toolbox.register('select', tools.selTournament, tournsize=3)

    pop = toolbox.population(n=100)

    # Evaluate the entire population.
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    NGEN = 100
    CXPB = 0.5
    MUTPB = 0.01

    # Begin the evolution.
    for g in xrange(NGEN):
        print '-- Generation %i --' % g

        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

            for mutant in offspring:
                if random.random() < MUTPB:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring

        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        print '    Min %s' % min(fits)
        print '    Max %s' % max(fits)
        print '    Avg %s' % mean
        print '    Std %s' % std

    print '-- End of (successful) evolution --'
    best_ind = tools.selBest(pop, 1)[0]
    print 'Best individual is %s, %s' % (best_ind, best_ind.fitness.values)


def main():
    one_max()


if __name__ == '__main__':
    main()

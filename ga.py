import random

from models import HRMAsm
from HRMEvals import mail_room_eval, busy_mail_room_eval, copy_floor_eval, scrambler_handler_eval, rainy_summer_eval, zero_exterminator_eval

def weighted_random_choice(population):
    tot_fit = 0
    for i in population:
        tot_fit += i.fitness
    pick = random.uniform(0, tot_fit)
    current = 0
    for individual in population:
        current += individual.fitness
        if current > pick:
            return individual

def generate_init_pop(size, struct_set, board_size):
    pop = []
    for i in range(size):
        temp = HRMAsm(struct_set, board_size)
        temp.generate_asm()
        pop.append(temp)

    return pop


def evaluate_fitness(population, initial_floor, fit_eval):
    k = 0
    for i in population:
        k += 1
        fit_eval(i, initial_floor)
        
def cull_pop(population, pop_reduc):
    population.sort(key = lambda x: x.fitness)
    k = 0
    while k < pop_reduc:
        population.pop(k)
        k += 1
        
def generate_gen(population, pop_inc, struct_set, board_size):
    new_pop = []
    for i in range(pop_inc):
        temp = HRMAsm(struct_set, board_size)
        temp.generate_asm()
        mutate_asm(temp)
        new_pop.append(temp)

    population.extend(new_pop)

def point_crossover(individual):
    pass

def mutate_asm(individual):
    if random.random() < 0.2:
        individual.add_new_instruction()
    if random.random() < 0.2:
        individual.remove_random_instruction()

def generic_main(instruct_set, initial_floor, pop_size, reduc_size, iterations, eval_func):
    pop = generate_init_pop(pop_size, instruct_set, len(initial_floor))
        
    for i in range(iterations):
        print "Iteration:", i
        evaluate_fitness(pop, initial_floor, eval_func)
        cull_pop(pop, reduc_size)
        generate_gen(pop, reduc_size, instruct_set, len(initial_floor))

    return pop

def mail_room_main():
    instruct_set = ['inbox', 'outbox']

    pop = generic_main(instruct_set, [], 100, 30, 100, mail_room_eval)

    print "Ending fitness"
    for i in pop:
        print i.fitness    
    best_answer = max(pop, key = lambda x : x.fitness)

    print "Best answer"
    print best_answer, best_answer.fitness
    
def busy_mail_room_main():
    instruct_set = ['inbox', 'outbox', 'jump']
    pop = generic_main(instruct_set, [], 260, 50, 100, busy_mail_room_eval)

    for i in pop:
        print i.fitness
    best_answer = max(pop, key = lambda x: x.fitness)
    print "Best answer"
    print best_answer, best_answer.fitness
    print "Final output"
    print best_answer.result_outbox

def copy_floor_main():
    instruct_set = ['inbox', 'outbox', 'jump', 'copyfrom']
    floor_set = ['U', 'J', 'X', 'G', 'B', 'E']
    pop = generic_main(instruct_set, floor_set, 260, 50, 4000, copy_floor_eval)

    for i in pop:
        print i.fitness
    best_answer = max(pop, key = lambda x: x.fitness)
    print "Best answer"
    print best_answer, best_answer.fitness
    print "Final output"
    print best_answer.result_outbox
    
def scrambler_handler():
    instruct_set = ['inbox', 'outbox', 'jump', 'copyfrom', 'copyto']
    floor_set = [None, None, None]
    pop = generic_main(instruct_set, floor_set, 260, 50, 4000, scrambler_handler_eval)

    for i in pop:
        print i.fitness
    best_answer = max(pop, key = lambda x: x.fitness)
    print "Best answer"
    print best_answer, best_answer.fitness
    print "Final output"
    print best_answer.result_outbox
    
def rainy_summer():
    instruct_set = ['inbox', 'outbox', 'jump', 'copyfrom', 'copyto', 'add']
    floor_set = [None, None, None]
    pop = generic_main(instruct_set, floor_set, 1000, 500, 40000, rainy_summer_eval)

    for i in pop:
        print i.fitness
    best_answer = max(pop, key = lambda x: x.fitness)
    print "Best answer"
    print best_answer, best_answer.fitness
    print "Final output"
    print best_answer.result_outbox


def zero_exterminator():
    instruct_set = ['inbox', 'outbox', 'jump', 'copyfrom', 'copyto', 'add', 'jump_0']
    floor_set = [None, None, None,
                 None, None, None,
                 None, None, None]
    pop = generic_main(instruct_set, floor_set, 1000, 430, 40000, zero_exterminator_eval)

    for i in pop:
        print i.fitness
    best_answer = max(pop, key = lambda x: x.fitness)
    print "Best answer"
    print best_answer, best_answer.fitness
    print "Final output"
    print best_answer.result_outbox

    
if __name__ == "__main__":
    # mail_room_main()
    # busy_mail_room_main()
    # copy_floor_main()
    # scrambler_handler()
    rainy_summer()
    # zero_exterminator()

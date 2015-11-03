
import random

from main import HRMAsm
from HRMEvals import mail_room_eval, busy_mail_room_eval

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


def evaluate_fitness(population, fit_eval):
    for i in population:
        fit_eval(i)
        
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

def mutate_asm(individual):
    if random.random() < 0.2:
        individual.add_new_instruction()
    if random.random() < 0.2:
        individual.remove_random_instruction()

def generic_main(instruct_set, board_size, pop_size, reduc_size, iterations, eval_func):
    pop = generate_init_pop(pop_size, instruct_set, board_size)
        
    for i in range(iterations):
        evaluate_fitness(pop, eval_func)
        cull_pop(pop, reduc_size)
        generate_gen(pop, reduc_size, instruct_set, board_size)

    return pop

def mail_room_main():
    instruct_set = ['inbox', 'outbox']

    pop = generic_main(instruct_set, 0, 100, 30, 100, mail_room_eval)

    print "Ending fitness"
    for i in pop:
        print i.fitness    
    best_answer = max(pop, key = lambda x : x.fitness)

    print "Best answer"
    print best_answer, best_answer.fitness
    
def busy_mail_room_main():
    instruct_set = ['inbox', 'outbox', 'jump']
    pop = generic_main(instruct_set, 0, 100, 30, 100, busy_mail_room_eval)

    for i in pop:
        print i.fitness
    best_answer = max(pop, key = lambda x: x.fitness)
    print "Best answer"
    print best_answer, best_answer.fitness

if __name__ == "__main__":
    # busy_mail_room_main()
    mail_room_main()

    

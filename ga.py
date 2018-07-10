import random
import os

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

def asm_crossover(p1, p2):

    # print " ASM crossover " 
    max_program_size = len(max([p1, p2], key = lambda x : len(x.program)).program)
    crossover_point = random.randint(0, max_program_size)

    # print p1
    # print p2 
    # print max_program_size
    # print crossover_point

    if random.random() < 0.5:
        # print "base is p1"
        base_copy = p1
        other_c = p2
    else:
        # print "base is p2"
        other_c = p1
        base_copy = p2

    new_asm = HRMAsm(base_copy.instruct_set, base_copy.max_size)
    
    for i in range(max_program_size):
        if i < crossover_point and i < len(base_copy.program):
            new_asm.add_instruction_from(base_copy.program[i])
        elif i < len(other_c.program):
            new_asm.add_instruction_from(other_c.program[i])
    return new_asm

def breed_pop(population, children_amount):
    children = []
    # print "Breed pop"

    for i in range(children_amount):
        p1 = weighted_random_choice(population)
        population.remove(p1)
        p2 = weighted_random_choice(population)
        population.append(p1)

        child = asm_crossover(p1, p2)
        children.append(child)
        # print "new child"
        # print child

    population.extend(children)

def mutate_asm(individual):
    if random.random() < 0.2:
        individual.add_new_instruction()
    if random.random() < 0.2:
        individual.remove_random_instruction()

def generic_main(instruct_set, initial_floor, pop_size, reduc_size, iterations, eval_func):
    pop = generate_init_pop(pop_size, instruct_set, len(initial_floor))
        
    for i in range(iterations):
        evaluate_fitness(pop, initial_floor, eval_func)
        cull_pop(pop, reduc_size)
        breed_pop(pop, 10)
        generate_gen(pop, reduc_size, instruct_set, len(initial_floor))
        if i % 100 == 0:
            print("Average fitness: ", sum([j.fitness for j in pop]) / len(pop))
        if i % 1000 == 0:
            print("Best fitness: ", (max(pop, key = lambda x: x.fitness)).fitness)
    return pop

def print_solution(problem, solution):
    solutions_folder = "HRMSolutions"
    os.mkdir(solutions_folder)
    solution_writer = open("%s/%s" % (solutions_folder, problem))
    solution_writer.write(str(solution))
    solution_writer.write("\n%s" % solution.fitness)
    solution_writer.close()

def mail_room_main():
    print("Mail room main")
    instruct_set = ['inbox', 'outbox']
    pop = generic_main(instruct_set, [], 100, 30, 100, mail_room_eval)

    best_answer = max(pop, key = lambda x : x.fitness)

    print("Best answer")
    print(best_answer, best_answer.fitness)
    
def busy_mail_room_main():
    print("Busy mail room main")
    instruct_set = ['inbox', 'outbox', 'jump']
    pop = generic_main(instruct_set, [], 260, 50, 100, busy_mail_room_eval)

    best_answer = max(pop, key = lambda x: x.fitness)
    print("Best answer")
    print(best_answer, best_answer.fitness)
    print("Final output")
    print(best_answer.result_outbox)

def copy_floor_main():
    print("Copy floor main")
    instruct_set = ['inbox', 'outbox', 'jump', 'copyfrom']
    floor_set = ['U', 'J', 'X', 'G', 'B', 'E']
    pop = generic_main(instruct_set, floor_set, 260, 50, 4000, copy_floor_eval)

    best_answer = max(pop, key = lambda x: x.fitness)
    print("Best answer")
    print(best_answer, best_answer.fitness)
    print("Final output")
    print(best_answer.result_outbox)
    
def scrambler_handler():
    print("Scrambler handler")
    instruct_set = ['inbox', 'outbox', 'jump', 'copyfrom', 'copyto']
    floor_set = [None, None, None]
    pop = generic_main(instruct_set, floor_set, 260, 50, 4000, scrambler_handler_eval)

    best_answer = max(pop, key = lambda x: x.fitness)
    print("Best answer")
    print(best_answer, best_answer.fitness)
    print("Final output")
    print(best_answer.result_outbox)
    
def rainy_summer():
    print("Rainy summer")
    instruct_set = ['inbox', 'outbox', 'jump', 'copyfrom', 'copyto', 'add']
    floor_set = [None, None, None]
    pop = generic_main(instruct_set, floor_set, 1000, 500, 40000, rainy_summer_eval)

    best_answer = max(pop, key = lambda x: x.fitness)
    print("Best answer")
    print(best_answer, best_answer.fitness)
    print("Final output")
    print(best_answer.result_outbox)

def zero_exterminator():
    print("Zero exterminator")
    instruct_set = ['inbox', 'outbox', 'jump', 'copyfrom', 'copyto', 'add', 'jump_0']
    floor_set = [None, None, None,
                 None, None, None,
                 None, None, None]
    pop = generic_main(instruct_set, floor_set, 1000, 430, 40000, zero_exterminator_eval)

    #for i in pop:
    #    print i.fitness
    best_answer = max(pop, key = lambda x: x.fitness)
    print("Best answer")
    print(best_answer, best_answer.fitness)
    print("Final output")
    print(best_answer.result_outbox)
    
if __name__ == "__main__":
    #mail_room_main()
    #busy_mail_room_main()
    #copy_floor_main()
    #scrambler_handler()
    #rainy_summer()
    zero_exterminator()

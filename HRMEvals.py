from main import HRMProgram, HRMAsm
import time

def length_eval(program):
    if len(program.asm.program) != 0:
        program.fitness += (100.0 / len(program.asm.program))

def min_eval(program):
    if program.fitness <= 0:
        program.fitness = 1

def finished_eval(program):
    if not program.finished_flag:
        program.fitness = 1

def mail_room_eval(individual):
    
    program = HRMProgram(individual, [1,2,3], [])

    program.run()

    if program.run_time_error:
        program.fitness = -100
    else:
        program.fitness = 10

    if program.outbox == [1,2,3]:
        program.fitness = 100

    length_eval(program)
    min_eval(program)

    individual.fitness = program.fitness

def busy_mail_room_eval(individual):
    program = HRMProgram(individual, ["i", "n", "i", "t", "i", "a", "l"], [])
    program.run()

if __name__ == "__main__":
    t = HRMAsm(['inbox', 'outbox'], 0)
    t.program.extend(['inbox', 'outbox', 'inbox', 'outbox', 'inbox', 'outbox'])
    mail_room_eval(t)

    print t.fitness

from main import HRMProgram, HRMAsm, HRMInstruct
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

def mail_room_eval(individual, initial_floor):
    
    program = HRMProgram(individual, [1,2,3], list(initial_floor))

    program.run()

    if program.run_time_error:
        program.fitness = -100.0
    else:
        program.fitness = 10.0

    if program.outbox == [1,2,3]:
        program.fitness = 100.0

    length_eval(program)
    min_eval(program)

    individual.fitness = program.fitness

def busy_mail_room_eval(individual, initial_floor):
    start = ['i', 'n', 'i', 't', 'i', 'a', 'l']
    program = HRMProgram(individual, list(start), list(initial_floor))
    program.run()

    if program.run_time_error:
        program.fitness = -100.0
    else:
        program.fitness = 10.0

    if program.outbox == start:
        program.fitness = 100.0

    #print program.outbox
    # length_eval(program)
    min_eval(program)
    
    individual.result_outbox = program.outbox
    individual.fitness = program.fitness


def copy_floor_eval(individual, initial_floor):
    start = [-99, -99, -99]
    correct_output = ["B", "U", "G"]
    program = HRMProgram(individual, list(start), list(initial_floor))

    program.run()

    if program.run_time_error:
        program.fitness = -100.0
    else:
        program.fitness = 10.0

    if len(program.outbox) == 3:
        program.fitness = 40.0    

    for i, j in zip(correct_output, program.outbox):
        if i == j:
            program.fitness += 30.0
    
        
    min_eval(program)

    individual.result_outbox = program.outbox
    individual.fitness = program.fitness
    
def output_data(individual):
    print individual.fitness

def mail_room_test():
    t = HRMAsm(['inbox', 'outbox'], 0)
    t.program.append(HRMInstruct('inbox'))
    t.program.append(HRMInstruct('outbox'))
    t.program.append(HRMInstruct('inbox'))
    t.program.append(HRMInstruct('outbox'))
    t.program.append(HRMInstruct('inbox'))
    t.program.append(HRMInstruct('outbox'))
    
    mail_room_eval(t)

    print t.fitness

def busy_mail_room_test():
    t = HRMAsm(['inbox', 'outbox', 'jump'], 0)
    t.program.append(HRMInstruct('inbox'))
    t.program.append(HRMInstruct('outbox'))
    jump = HRMInstruct('jump')
    jump.ref_value = 0
    t.program.append(jump)
    busy_mail_room_eval(t)

    print t.fitness


def copy_floor_test():
    t = HRMAsm(['inbox', 'outbox', 'jump', 'copyfrom'], 6)
    cp = HRMInstruct('copyfrom')
    cp.ref_value = 1
    t.program.append(cp)
    t.program.append(HRMInstruct('outbox'))
    cp = HRMInstruct('copyfrom')
    cp.ref_value = 0
    t.program.append(cp)
    t.program.append(HRMInstruct('outbox'))
    t.program.append(HRMInstruct('inbox'))
    t.program.append(HRMInstruct('outbox'))
    cp = HRMInstruct('jump')
    cp.ref_value = 7
    t.program.append(cp)
    cp = HRMInstruct('copyfrom')
    cp.ref_value = 4
    t.program.append(cp)
    floor_set = ['U', 'B', 'A', 'G', 'K', 'Z']

    copy_floor_eval(t, floor_set)
    
    print t.fitness

if __name__ == "__main__":
    # busy_mail_room_test()
    copy_floor_test()

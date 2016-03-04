import random

HRM_full_instruction_set = {'inbox', 'outbox'}

# a single instance of an instruction
# is basically an identifier
class HRMInstruct(object):
    def __init__(self, instruct):
        if type(instruct) == type(""):
            self.instruct = instruct
        elif type(instruct) == HRMInstruct:
            self.copy(instruct)

        self.ref_value = -1

    def __str__(self):
        if self.instruct == "jump":
            return str(self.instruct) + " " + str(self.ref_value)
        elif self.instruct == "copyfrom":
            return str(self.instruct) + " " + str(self.ref_value)
        elif self.instruct == "copyto":
            return str(self.instruct) + " " + str(self.ref_value)
        elif self.instruct == "add":
            return str(self.instruct) + " " + str(self.ref_value)
        elif self.instruct == "jump_0":
            return str(self.instruct) + " " + str(self.ref_value)
        return str(self.instruct)

    def copy(self, cpy):
        self.instruct == cpy.instruct

# probably unused
class HRMBox(object):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return str(self.data)


# An entire program which contains a inbox, outbox, a list of instructions
# has a max jump counter to limit the possible number of jumps that can be made
class HRMProgram(object):

    def __init__(self, instruct_list, inbox, floor):
        self.holder = None
        self.run_time_error = False
        self.finished_flag = False
        self.floor_spaces = list(floor)
        self.asm = instruct_list
        self.inbox = list(inbox)
        self.outbox = []
        self.program_counter = 0
        self.max_jump_count = 100
        self.jump_count = 0
        if len(self.floor_spaces) != self.asm.max_size:
            print "Error size incorrect"

    def run(self):

        while not self.finished_flag:
            if self.program_counter >= len(self.asm.program) or self.program_counter < 0:
                print "Error with program counter", self.program_counter, len(self.asm.program)
                self.run_time_error = True

            if self.run_time_error:
                # print "Error run time error"    
                break

            current_instruction = self.asm.program[self.program_counter]

            if current_instruction.instruct == "inbox":
                self._inbox()
            elif current_instruction.instruct == "outbox":
                self._outbox()
            elif current_instruction.instruct == "jump":
                self._jump()
            elif current_instruction.instruct == "copyfrom":
                self._copyfrom()
            elif current_instruction.instruct == "copyto":
                self._copyto()
            elif current_instruction.instruct == "add":
                self._add()
            elif current_instruction.instruct == "jump_0":
                self._jump_zero()
            else:
                self.run_time_error = True

    def _inbox(self):
        if len(self.inbox) <= 0:
            # print "Finished Execution"
            self.finished_flag = True
            return
        self.holder = self.inbox.pop(0)

        self._inc_prog_counter()

    def _outbox(self):
        if self.holder == None:
            # print "Empy value! You can't OUTBOX with empty hands!"
            self.run_time_error = True
            return
        self.outbox.append(self.holder)
        self.holder = None

        self._inc_prog_counter()

    def _jump(self):
        self.jump_count += 1
        if self.jump_count >= self.max_jump_count:
            # print "To many jumps"
            self.run_time_error = True
            return
        
        instruct = self.asm.program[self.program_counter]
        self.program_counter = instruct.ref_value

    def _copyfrom(self):
        instruct = self.asm.program[self.program_counter]
        if not self.floor_spaces[instruct.ref_value]:
            # print "Error no value on floor"
            self.run_time_error = True
            return 

        self.holder = self.floor_spaces[instruct.ref_value]
        
        self._inc_prog_counter()

    def _copyto(self):
        instruct = self.asm.program[self.program_counter]
        self.floor_spaces[instruct.ref_value] = self.holder
        self._inc_prog_counter()

    def _add(self):
        instruct = self.asm.program[self.program_counter]
        if not self.floor_spaces[instruct.ref_value]:
            # print "Error no value on floor"
            self.run_time_error = True
            return
        if type(self.holder) != type(0):
            self.run_time_error = True
            return
        self.holder = self.holder + self.floor_spaces[instruct.ref_value]
        self._inc_prog_counter()

    def _jump_zero(self):
        if self.holder is None:
            self.run_time_error = True
            return
        
        if self.holder == 0:
            self.jump_count += 1
            if self.jump_count >= self.max_jump_count:
                self.run_time_error = True
                return
            
            instruct = self.asm.program[self.program_counter]
            self.program_counter = instruct.ref_value
        else:
            self._inc_prog_counter()

    def _inc_prog_counter(self):
        if self.program_counter + 1 < len(self.asm.program):
            self.program_counter += 1
        elif self.program_counter + 1 >= len(self.asm.program):
            # print "Reached end of program"
            self.finished_flag = True
    
    def __str__(self):
        return str(self.asm)


# HRM ASM is a set of instructions 
class HRMAsm(object):
    def __init__(self, instruct_set, board_size):
        self.max_size = board_size
        self.instruct_set = instruct_set
        self.instruct_size = len(self.instruct_set)
        self.program = []
        self.fitness = 0

    def __str__(self):
        msg = ""
        for i in self.program:
            msg += "%s\n" % i
        return msg

    def generate_asm(self):
        for i in range(random.randint(3, 10)):
            self.add_new_instruction()

    def add_new_instruction(self):
        self.program.append(self.get_random_instruction())
    
    def remove_random_instruction(self):
        self.program.remove(self.program[random.randint(0, len(self.program)-1)])
        if len(self.program) == 0:
            self.add_new_instruction()

    def get_random_instruction(self):

        new_instruct = HRMInstruct(self.instruct_set[random.randint(0, len(self.instruct_set)-1)])
        if new_instruct.instruct == 'jump':
            new_instruct.ref_value = random.randint(0, len(self.program))
        elif new_instruct.instruct == 'copyfrom' or new_instruct.instruct == 'copyto' or new_instruct.instruct == "add":
            new_instruct.ref_value = random.randint(0, self.max_size-1)
        elif new_instruct.instruct == 'jump_0':
            new_instruct.ref_value == random.randint(0, len(self.program))
            

        return new_instruct

if __name__ == "__main__":
    p = HRMAsm(['inbox', 'outbox'], 0)
    p.generate_asm()
    print p.program
    print p
    
    

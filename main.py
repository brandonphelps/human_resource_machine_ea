import random

HRM_full_instruction_set = {'inbox', 'outbox'}


class HRMInstruct(object):
    def __init__(self, instruct):
        if type(instruct) == type(""):
            self.instruct = instruct
        elif type(instruct) == HRMInstruct:
            self.copy(instruct)

        self.jump_loc = -1

    def __str__(self):
        return self.instruct

    def copy(self, cpy):
        self.instruct == cpy.instruct


class HRMBox(object):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return str(self.data)

        
class HRMProgram(object):

    def __init__(self, instruct_list, inbox, floor):
        self.holder = None
        self.run_time_error = False
        self.finished_flag = False
        self.floor_spaces = floor
        self.asm = instruct_list
        self.inbox = inbox
        self.outbox = []
        self.program_counter = 0
        if len(self.floor_spaces) != self.asm.max_size:
            print "Error size incorrect"

    def run(self):
        # print "Starting Run"

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
            else:
                self.run_time_error = True
            self.program_counter += 1

        t = """
        for i in self.asm.program:
            if self.finished_flag:
                break
            if self.run_time_error:
                # print "Runtime error"
                break
            if i.instruct == "inbox":
                self._inbox()
            elif i.instruct == "outbox":
                self._outbox()
            elif i.instruct == "jump":
                self._jump()
            else:
                self.run_time_error = True
        """

    def _inbox(self):
        if len(self.inbox) <= 0:
            # print "Finished Execution"
            self.finished_flag = True
            return
        self.holder = self.inbox.pop(0)

    def _outbox(self):
        if self.holder == None:
            # print "Empy value! You can't OUTBOX with empty hands!"
            self.run_time_error = True
            return
        self.outbox.append(self.holder)
        self.holder = None
        
    def _jump(self):
        pass

    def __str__(self):
        return str(self.asm)


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
            # self.program.append(self.get_random_instruction())
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
            print "Making a jump instruct"
            new_instruct.jump_loc = random.randint(0, len(self.program))
            print "Setting jump loc to", new_instruct.jump_loc
        return new_instruct

if __name__ == "__main__":
    p = HRMAsm(['inbox', 'outbox'], 0)
    p.generate_asm()
    print p
    
    

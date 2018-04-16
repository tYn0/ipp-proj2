import xml.etree.ElementTree as ET
import sys
import re

class Instruction:
    """Class representing an instruction"""

    def __init__(self, order):
        self.order = int(order)
        self.ops_list = list()
        self.opcode = None
        self.interpreter = Interpreter.getInstance()

    def addOperand(self, operand=None):
        if operand is None:
            self.interpreter.raiseError(99, "Trying to add empty operand, exiting...")
        self.ops_list.append(operand)

    def printOperands(self):
        #Check if we have any operands
        if not self.ops_list:
            print("The instruction has no operands")
            return

        for i, op in enumerate(self.ops_list):
            print("Operand", i)
            print("\tOperand type:", op.v_type)
            print("\tOperand value:", op.value)

    def printInstruction(self):
        print("Instruction {0} order {1}:".format(self.opcode, self.order))
        self.printOperands()

    def printExecuting(self):
        return
        print("Instruction {0} executing, order is {1}, counter is {2}".format(self.opcode, self.order, self.interpreter.instructionCounter) )

class Ins_POPFRAME(Instruction):
    """POPFRAME instruction"""

    def __init__(self, order):
        super(Ins_POPFRAME, self).__init__(order)
        self.opcode = "POPFRAME"

    def execute(self):
        self.printExecuting()
        self.interpreter.popFrame()

class Ins_PUSHFRAME(Instruction):
    """PUSHFRAME instruction"""

    def __init__(self, order):
        super(Ins_PUSHFRAME, self).__init__(order)
        self.opcode = "PUSHFRAME"

    def execute(self):
        self.printExecuting()
        self.interpreter.pushFrame()

class Ins_CREATEFRAME(Instruction):
    """CREATEFRAME instruction"""

    def __init__(self, order):
        super(Ins_CREATEFRAME, self).__init__(order)
        self.opcode = "CREATEFRAME"

    def execute(self):
        self.printExecuting()
        self.interpreter.createTempFrame()

class Ins_DEFVAR(Instruction):
    """DEFVAR instruction"""

    def __init__(self, order):
        super(Ins_DEFVAR, self).__init__(order)
        self.opcode = "DEFVAR"

    def execute(self):
        self.printExecuting()
        #self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        operand = self.ops_list[0].getValue()
        #Check if variable exists in given frame
        frame = operand[0] # Frame
        name = operand[1] # Variable name
        ret = self.interpreter.getVarFromFrame(frame, name)

        #If we get -1, variable does not exist in the frame and we can add it
        if ret == -1:
            var = Variable(name) #Create new variable
            self.interpreter.addVarToFrame(frame, var)
        else:
            self.interpreter.raiseError(54, "Variable already exists in frame {0}, exiting...".format(frame))

class Ins_MOVE(Instruction):
    """MOVE instruction"""

    def __init__(self, order):
        super(Ins_MOVE, self).__init__(order)
        self.opcode = "MOVE"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)

        #Get var1 and var2
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()

        var1.var_type = var2.var_type

        if var2.getValue() is None:
            if var1.var_type == "string":
                var1.value = ""
            elif var1.var_type == "int":
                var1.value = 0
            elif var1.var_type == "bool":
                var1.value = "false"
        else:
            var1.value = var2.getValue()

class Ins_LABEL(Instruction):
    """LABEL instruction"""

    def __init__(self, order):
        super(Ins_LABEL, self).__init__(order)
        self.opcode = "LABEL"

    def execute(self):
        self.printExecuting()
        #self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var = self.ops_list[0].toVar()
        label = var.getValue()
        self.interpreter.addLabel(label, self.order)

class Ins_JUMP(Instruction):
    """JUMP instruction"""

    def __init__(self, order):
        super(Ins_JUMP, self).__init__(order)
        self.opcode = "JUMP"

    def execute(self):
        self.printExecuting()
        #self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var = self.ops_list[0].toVar()
        label = var.getValue()
        self.interpreter.jumpToLabel(label)

class Ins_JUMPIFEQ(Instruction):
    """JUMPIFEQ instruction"""

    def __init__(self, order):
        super(Ins_JUMPIFEQ, self).__init__(order)
        self.opcode = "JUMPIFEQ"

    def execute(self):
        self.printExecuting()
        #self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()
        var3 = self.ops_list[2].toVar()

        label = var1.getValue()

        #Compare the types
        if var2.var_type != var3.var_type:
            # TODO: Better error handling
            print("Trying to compare two values of different type, exiting...")
            exit(53)

        #Compare the values
        if var2.getValue() == var3.getValue():
            self.interpreter.jumpToLabel(label)

class Ins_JUMPIFNEQ(Instruction):
    """JUMPIFNEQ instruction"""

    def __init__(self, order):
        super(Ins_JUMPIFNEQ, self).__init__(order)
        self.opcode = "JUMPIFNEQ"

    def execute(self):
        self.printExecuting()
        #self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()
        var3 = self.ops_list[2].toVar()

        label = var1.getValue()

        #Compare the types
        if var2.var_type != var3.var_type:
            # TODO: Better error handling
            print("Trying to compare two values of different type, exiting...")
            exit(53)

        #Compare the values
        if var2.getValue() != var3.getValue():
            self.interpreter.jumpToLabel(label)

class Ins_ADD(Instruction):
    """ADD instruction"""

    def __init__(self, order):
        super(Ins_ADD, self).__init__(order)
        self.opcode = "ADD"

    def execute(self):
        self.printExecuting()
        #self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()
        var3 = self.ops_list[2].toVar()

        if var2.var_type != "int" or var3.var_type != "int":
            # TODO: Better error handling
            print("Trying to ADD two values of different type, exiting...")
            exit(53)

        var1.var_type = "int"
        var1.value = var2.getValue() + var3.getValue()

class Ins_SUB(Instruction):
    """SUB instruction"""

    def __init__(self, order):
        super(Ins_SUB, self).__init__(order)
        self.opcode = "SUB"

    def execute(self):
        self.printExecuting()
        #self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()
        var3 = self.ops_list[2].toVar()

        if var2.var_type != "int" or var3.var_type != "int":
            # TODO: Better error handling
            print("Trying to SUB two values of different type, exiting...")
            exit(53)

        var1.var_type = "int"
        var1.value = var2.getValue() - var3.getValue()

class Ins_MUL(Instruction):
    """MUL instruction"""

    def __init__(self, order):
        super(Ins_MUL, self).__init__(order)
        self.opcode = "MUL"

    def execute(self):
        self.printExecuting()
        #self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()
        var3 = self.ops_list[2].toVar()

        if var2.var_type != "int" or var3.var_type != "int":
            # TODO: Better error handling
            print("Trying to MUL two values of different type, exiting...")
            exit(53)

        var1.var_type = "int"
        var1.value = var2.getValue() * var3.getValue()

class Ins_IDIV(Instruction):
    """IDIV instruction"""

    def __init__(self, order):
        super(Ins_IDIV, self).__init__(order)
        self.opcode = "IDIV"

    def execute(self):
        self.printExecuting()
        #self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()
        var3 = self.ops_list[2].toVar()

        if var2.var_type != "int" or var3.var_type != "int":
            # TODO: Better error handling
            print("Trying to IDIV two values of different type, exiting...")
            exit(53)

        if var3.getValue() == 0:
            # TODO: Better error handling
            print("Trying to divide by zero, exiting...")
            exit(57)

        var1.var_type = "int"
        var1.value = var2.getValue() // var3.getValue()

class Ins_LT(Instruction):
    """LT instruction"""

    def __init__(self, order):
        super(Ins_LT, self).__init__(order)
        self.opcode = "LT"

    def execute(self):
        self.printExecuting()
        #self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()
        var3 = self.ops_list[2].toVar()

        if var2.var_type != var3.var_type:
            # TODO: Better error handling
            print("Trying to compare two values of different type, exiting...")
            exit(53)

        var1.var_type = var2.var_type

        if var2.getValue() < var3.getValue():
            var1.value = "true"
        else:
            var1.value = "false"

class Ins_GT(Instruction):
    """GT instruction"""

    def __init__(self, order):
        super(Ins_GT, self).__init__(order)
        self.opcode = "GT"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()
        var3 = self.ops_list[2].toVar()

        if var2.var_type != var3.var_type:
            # TODO: Better error handling
            print("Trying to compare two values of different type, exiting...")
            exit(53)

        var1.var_type = var2.var_type

        if var2.getValue() > var3.getValue():
            var1.value = "true"
        else:
            var1.value = "false"

class Ins_EQ(Instruction):
    """EQ instruction"""

    def __init__(self, order):
        super(Ins_EQ, self).__init__(order)
        self.opcode = "EQ"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()
        var3 = self.ops_list[2].toVar()

        if var2.var_type != var3.var_type:
            # TODO: Better error handling
            print("Trying to compare two values of different type, exiting...")
            exit(53)

        var1.var_type = var2.var_type

        if var2.getValue() == var3.getValue():
            var1.value = "true"
        else:
            var1.value = "false"

class Ins_AND(Instruction):
    """AND instruction"""

    def __init__(self, order):
        super(Ins_AND, self).__init__(order)
        self.opcode = "AND"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()
        var3 = self.ops_list[2].toVar()

        if var2.var_type != "bool" or var3.var_type != "bool":
            # TODO: Better error handling
            print("Trying to compare two values of different type, exiting...")
            exit(53)

        var1.var_type = "bool"

        if var2.getValue() == "true" and var3.getValue() == "true":
            var1.value = "true"
        else:
            var1.value = "false"

class Ins_OR(Instruction):
    """OR instruction"""

    def __init__(self, order):
        super(Ins_OR, self).__init__(order)
        self.opcode = "OR"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()
        var3 = self.ops_list[2].toVar()

        if var2.var_type != "bool" or var3.var_type != "bool":
            # TODO: Better error handling
            print("Trying to compare two values of different type, exiting...")
            exit(53)

        var1.var_type = "bool"

        if var2.getValue() == "true" or var3.getValue() == "true":
            var1.value = "true"
        else:
            var1.value = "false"

class Ins_NOT(Instruction):
    """NOT instruction"""

    def __init__(self, order):
        super(Ins_NOT, self).__init__(order)
        self.opcode = "NOT"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()

        if var2.var_type != "bool":
            # TODO: Better error handling
            print("Trying to NOT a non-boolean value, exiting...")
            exit(53)

        var1.var_type = "bool"

        if var2.getValue() == "true":
            var1.value = "false"
        else:
            var1.value = "true"

class Ins_INT2CHAR(Instruction):
    """INT2CHAR instruction"""

    def __init__(self, order):
        super(Ins_INT2CHAR, self).__init__(order)
        self.opcode = "INT2CHAR"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()

        if var2.var_type != "int":
            # TODO: Better error handling
            print("Trying to convert non-int value, exiting...")
            exit(53)

        if var2.getValue() >= 1114112:
            # TODO: Better error handling
            print("Trying to convert out of range value, exiting...")
            exit(58)

        var1.var_type = "string"
        var1.value = chr(var2.getValue())

class Ins_STRI2INT(Instruction):
    """STRI2INT instruction"""

    def __init__(self, order):
        super(Ins_STRI2INT, self).__init__(order)
        self.opcode = "STRI2INT"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()
        var2 = self.ops_list[2].toVar()

        if var2.var_type != "string" or var3.var_type != "int":
            # TODO: Better error handling
            print("Wrong type, exiting...")
            exit(53)

        lenght = len(var2.getValue())-1

        if var3.getValue() > lenght or var3.getValue() < 0:
            # TODO: Better error handling
            print("Out of bounds, exiting...")
            exit(58)


        index = var3.getValue()
        value = ord(var2.getValue()[index]) #Access the character on index position

        var1.var_type = "int"
        var1.value = value

class Ins_WRITE(Instruction):
    """WRITE instruction"""

    def __init__(self, order):
        super(Ins_WRITE, self).__init__(order)
        self.opcode = "WRITE"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)

        #Get var1
        var1 = self.ops_list[0].toVar()

        #Print it
        print(var1.getValue())

class Ins_READ(Instruction):
    """READ instruction"""

    def __init__(self, order):
        super(Ins_READ, self).__init__(order)
        self.opcode = "READ"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)

        #Get vars
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()

        if var2.var_type != "type":
            # TODO: Better error handling
            print("Wrong type, exiting...")
            exit(53)

        if var2.getValue() not in {"int","bool","string"}:
            # TODO: Better error handling
            print("Wrong type, exiting...")
            exit(53)

        convertTo = var2.getValue()

        if convertTo == "int":
            var1.value = 0
        elif convertTo == "string":
            var1.value = ""
        elif convertTo == "bool":
            var1.value = "false"

        var1.var_type = convertTo

        inp = input()
        var1.value = inp

        if convertTo == "bool":
            if inp.lower() == "true":
                var1.value = "true"
            else:
                var1.value = "false"

class Ins_CONCAT(Instruction):
    """CONCAT instruction"""

    def __init__(self, order):
        super(Ins_CONCAT, self).__init__(order)
        self.opcode = "CONCAT"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()
        var3 = self.ops_list[2].toVar()

        if var2.var_type != "string" or var3.var_type != "string":
            # TODO: Better error handling
            print("Trying to concatenate non-string value, exiting...")
            exit(53)

        var1.var_type = "string"
        var1.value =  var2.getValue() + var3.getValue()

class Ins_STRLEN(Instruction):
    """STRLEN instruction"""

    def __init__(self, order):
        super(Ins_STRLEN, self).__init__(order)
        self.opcode = "STRLEN"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()

        if var2.var_type != "string":
            # TODO: Better error handling
            print("Trying to get length of non-string value, exiting...")
            exit(53)

        var1.var_type = "int"
        var1.value =  len(var2.getValue())

class Ins_GETCHAR(Instruction):
    """GETCHAR instruction"""

    def __init__(self, order):
        super(Ins_GETCHAR, self).__init__(order)
        self.opcode = "GETCHAR"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()
        var3 = self.ops_list[2].toVar()

        if var2.var_type != "string" or var3.var_type != "int":
            # TODO: Better error handling
            print("Wrong types, exiting...")
            exit(53)

        lenght = len(var2.getValue()) - 1

        if var3.getValue() > lenght or var3.getValue() < 0:
            # TODO: Better error handling
            print("Out of bounds, exiting...")
            exit(58)

        index = var3.getValue()
        value = var2.getValue()[index]

        var1.var_type = "string"
        var1.value = value

class Ins_SETCHAR(Instruction):
    """SETCHAR instruction"""

    def __init__(self, order):
        super(Ins_SETCHAR, self).__init__(order)
        self.opcode = "SETCHAR"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()
        var3 = self.ops_list[2].toVar()

        if var1.var_type != "string" or var2.var_type != "int" or var3.var_type != "string":
            # TODO: Better error handling
            print("Wrong types, exiting...")
            exit(53)

        lenght = len(var1.getValue()) - 1

        if var2.getValue() > lenght or var2.getValue() < 0:
            # TODO: Better error handling
            print("Out of bounds, exiting...")
            exit(58)

        #If the length of string in var3 is more than 1, use the first character
        index = var2.getValue()
        if(len(var3.getValue()) > 1):
            var1.value[index] = var3.getValue()[0]
        else:
            var1.value[index] = var3.getValue()

class Ins_TYPE(Instruction):
    """TYPE instruction"""

    def __init__(self, order):
        super(Ins_TYPE, self).__init__(order)
        self.opcode = "TYPE"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()
        var2 = self.ops_list[1].toVar()

        var1.var_type = "string"
        if var2.var_type is None:
            var1.value = ""
        else:
            var1.value = var2.var_type

class Ins_DPRINT(Instruction):
    """DPRINT instruction"""

    def __init__(self, order):
        super(Ins_DPRINT, self).__init__(order)
        self.opcode = "DPRINT"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        var1 = self.ops_list[0].toVar()

        print(var1.getValue(), file=sys.stderr)

class Ins_BREAK(Instruction):
    """BREAK instruction"""

    def __init__(self, order):
        super(Ins_BREAK, self).__init__(order)
        self.opcode = "BREAK"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)

        self.interpreter.debugInfo()

class Ins_PUSHS(Instruction):
    """PUSHS instruction"""

    def __init__(self, order):
        super(Ins_PUSHS, self).__init__(order)
        self.opcode = "PUSHS"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)

        var1 = self.ops_list[0].toVar()

        self.interpreter.stackPUSHS(var1)

class Ins_POPS(Instruction):
    """POPS instruction"""

    def __init__(self, order):
        super(Ins_POPS, self).__init__(order)
        self.opcode = "POPS"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)

        var1 = self.ops_list[0].toVar()

        ret = self.interpreter.stackPOPS()

        if ret == -1:
            # TODO: Better error handling
            print("Trying to pop an empty stack, exiting...")
            exit(56)

        var1 = ret

class Ins_CALL(Instruction):
    """CALL instruction"""

    def __init__(self, order):
        super(Ins_CALL, self).__init__(order)
        self.opcode = "CALL"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)

        var1 = self.ops_list[0].toVar()
        if var1.var_type != "label":
            # TODO: Better error handling
            print("Wrong type, exiting...")
            exit(53)

        label = var1.getValue()
        self.interpreter.insCall(label,self.order)

class Ins_RETURN(Instruction):
    """RETURN instruction"""

    def __init__(self, order):
        super(Ins_RETURN, self).__init__(order)
        self.opcode = "RETURN"

    def execute(self):
        self.printExecuting()
        # self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        ret = self.interpreter.insReturn()
        if ret == -1:
            # TODO: Better error handling
            print("Trying to pop empty callstack, exiting...")
            exit(56)

class Operand:
    """Class representing single operand of an instruction"""

    def __init__(self, v_type, value):
        self.v_type = v_type
        self.value = value

    def check(self):
        """Checks if the operand is valid"""

        #Literal without value (int,string or bool), nothing to check
        if self.value is None and self.v_type in {"int","bool","string"}:
            return
        elif self.value is None:
            Interpreter.getInstance().raiseError(52, "No value, exiting...")

        if self.v_type == "int":
            p = re.compile("^-?\d*$") #Regular expressions are black magic
            m = p.match(self.value)
            if m:
                self.value = int(self.value)
            else:
                Interpreter.getInstance().raiseError(52, "Expected integer number, exiting...")

        elif self.v_type == "bool":
            if self.value != "true" or self.value != "false":
                Interpreter.getInstance().raiseError(52, "Expected boolean value, exiting...")
        elif self.v_type == "string":
            pass # TODO :/
        elif self.v_type == "label":
            self.checkName(self.value)
        elif self.v_type == "type":
            if self.value not in {"int", "bool", "string"}:
                Interpreter.getInstance().raiseError(52, "Non-existing type {0}, exiting...".format(self.value))
        elif self.v_type == "var":
            split = self.value.split("@")
            if len(split) != 2: #We need a list with exactly 2 strings
                Interpreter.getInstance().raiseError(52, "Wrong variable definition, exiting...")
            frame = split[0]
            name = split[1]
            #Check the frame
            if frame not in {"GF","TF","LF"}:
                Interpreter.getInstance().raiseError(52, "Invalid frame {0}, exiting...".format(frame))
            #Check the name
            self.checkName(name)
        else:
            Interpreter.getInstance().raiseError(52, "Non-existing type {0}, exiting...".format(self.v_type))

    def checkName(self, name):
        p = re.compile("^[A-Za-z_$*&%-]{1}[A-Z0-9a-z_$*&%-]*$")  # First character cannot be a number
        m = p.match(name)
        if not m:
            Interpreter.getInstance().raiseError(52, "Name {0} contains illegal character, exiting...".format(name))

    def toVar(self):
        self.check()
        if self.v_type == "var":
            split = self.value.split("@")
            frame = split[0]
            name = split[1]

            #Get variable from specified frame
            var = Interpreter.getInstance().getVarFromFrame(frame, name)
            if var == -1:
                Interpreter.getInstance().raiseError(54, "Variable does not exists in frame {0}, exiting...".format(frame))
            return var
        elif self.v_type in {"int","bool","string","label","type"}:
            return Variable("literal", self.value, self.v_type)

    def getValue(self):
        self.check()
        if self.v_type == "int":
            return self.value
        elif self.v_type == "bool":
            return self.value
        elif self.v_type == "string":
            return self.value
        elif self.v_type == "label":
            return self.value
        elif self.v_type == "type":
            return self.value
        elif self.v_type == "var":
            return self.value.split("@")

class Variable:
    """Class representing single variable to be stored in a frame"""

    def __init__(self, name, value=None, var_type=None):
        self.name = name
        self.value = value
        self.var_type = var_type

    def getValue(self):
        if self.var_type is None:
            Interpreter.getInstance().raiseError(56, "Trying to access uninitialized variable {0}, exiting...".format(self.name))
        return self.value

    def printVar(self):
        print("Variable '{0}' has value '{1}' and type '{2}'".format(self.name,self.value,self.var_type))

class Frame:
    """Class representing a single frame"""

    def __init__(self):
        self.content = list()

    def addVar(self, var=None):
        if var is None:
            Interpreter.getInstance().raiseError(99, "Trying to add empty variable, exiting...")
        self.content.append(var)

    def getVar(self,name):
        for v in self.content:
            if v.name == name:
                return v
        return -1

    def printFrame(self):
        for var in self.content:
            var.printVar()

class Interpreter:
    """Class representing interpreter"""

    __instance = None #Reference to instance

    #We want this class to be a singleton
    @staticmethod
    def getInstance():
        """ Get static instance"""
        if Interpreter.__instance == None:
            Interpreter()
        return Interpreter.__instance

    def __init__(self,file):
        if Interpreter.__instance != None:
            raise Exception("Interpreter class is singleton")
        else:
            Interpreter.__instance = self

        self.instruction_list = list()
        self.label_list = list()
        self.instructionCounter = int()

        self.varStack = list() #Stack of variables to be used with POPS and PUSHS
        self.callStack = list() #Holds instruction number to return to on RETURN instruction
        self.frameStack = list() #Stack of frames

        self.localFrame = None #Local frame reference
        self.tempFrame = None #Temporary frame reference
        self.globalFrame = Frame() #Global frame reference

        self.loadFromXML(file)

    def raiseError(self, errcode, message=None):
        print(message)
        exit(errcode)

    def getLocalFrame(self):
        if self.localFrame is None:
            self.raiseError(55, "No local frame, exiting...")

        return self.localFrame

    def getTempFrame(self):
        if self.tempFrame is None:
            self.raiseError(55, "No temporary frame, exiting...")

        return self.tempFrame

    def getGlobalFrame(self):
        return self.globalFrame

    def getVarFromFrame(self,frame,name):
        if(frame == "GF"):
            var = self.getGlobalFrame().getVar(name)
        elif (frame == "LF"):
            var = self.getLocalFrame().getVar(name)
        elif (frame == "TF"):
            var = self.getTempFrame().getVar(name)

        return var

    def addVarToFrame(self,frame,var):
        if (frame == "GF"):
            self.getGlobalFrame().addVar(var)
        elif (frame == "LF"):
            self.getLocalFrame().addVar(var)
        elif (frame == "TF"):
            self.getTempFrame().addVar(var)

    def dumpFrames(self):
        print("Global frame:")
        self.getGlobalFrame().printFrame()

        if(self.localFrame is not None):
            print("Local frame:")
            self.getLocalFrame().printFrame()

        if (self.tempFrame is not None):
            print("Temporary frame:")
            self.getTempFrame().printFrame()

    def createTempFrame(self):
        self.tempFrame = Frame()

    def pushFrame(self):
        if self.tempFrame is None:
            self.raiseError(55,"No temporary frame, exiting...")

        self.frameStack.append(self.tempFrame) #Push tempFrame to stack
        self.refreshLocalFrame() #Set new local frame
        self.tempFrame = None #Deinitialize tempFrame

    def popFrame(self):
        if self.localFrame is None:
            self.raiseError(55,"No local frame, exiting...")

        self.tempFrame = self.frameStack.pop() #Pop the stack
        self.refreshLocalFrame() #Refresh to new localFrame

    def refreshLocalFrame(self):
        if len(self.frameStack) == 0:
            self.frameStack = list() #frameStack is empty, reinitialize it
            self.localFrame = None #The stack is empty, there is no localFrame
        else:
            self.localFrame = self.frameStack[-1] #Set localFrame to the top of the stack

    def addLabel(self,label,order):
        """Adds label to the list of labels"""
        if (self.findLabel(label) != -1):
            self.raiseError(52,"Label {0} already defined, exiting...".format(label))

        #Seems fine, add to the label list
        self.label_list.append({label: order})

    def jumpToLabel(self, label):
        label_dict = self.findLabel(label)
        if (label_dict == -1):
            self.raiseError(52, "Label {0} is not defined, exiting...".format(label))

        #Set the instruction counter to the label position
        #print("Jumping to instruction number {0}".format(label_dict[label]+1))
        self.instructionCounter = label_dict[label]


    def findLabel(self, label):
        """Finds specified label in list, if the label is undefined it returns -1"""
        for d in self.label_list:
            if label in d:
                return d
        return -1

    def debugInfo(self):
        print("Instruction counter = {0}".format(self.instructionCounter),file = sys.stderr)

    def stackPOPS(self):
        if len(self.varStack) == 0:
            return -1
        return self.varStack.pop()

    def stackPUSHS(self, var):
        self.varStack.append(var)

    def insCall(self,label,order):
        self.callStack.append(order)
        self.jumpToLabel(label)

    def insReturn(self):
        if len(self.callStack) == 0:
            return -1
        jumpTo = self.callStack.pop()
        self.instructionCounter = jumpTo

    def generateInstruction(self, opcode, order):
        """Generates empty(without operands)instruction according to opcode"""

        instructions = {"DEFVAR": Ins_DEFVAR(order),
                        "MOVE": Ins_MOVE(order),
                        "CREATEFRAME": Ins_CREATEFRAME(order),
                        "PUSHFRAME": Ins_PUSHFRAME(order),
                        "POPFRAME": Ins_POPFRAME(order),
                        "LABEL": Ins_LABEL(order),
                        "JUMP": Ins_JUMP(order),
                        "JUMPIFEQ": Ins_JUMPIFEQ(order),
                        "JUMPIFNEQ": Ins_JUMPIFNEQ(order),
                        "ADD": Ins_ADD(order),
                        "SUB": Ins_SUB(order),
                        "MUL": Ins_MUL(order),
                        "IDIV": Ins_IDIV(order),
                        "LT": Ins_LT(order),
                        "GT": Ins_GT(order),
                        "EQ": Ins_EQ(order),
                        "AND": Ins_AND(order),
                        "OR": Ins_OR(order),
                        "NOT": Ins_NOT(order),
                        "INT2CHAR": Ins_INT2CHAR(order),
                        "STRI2INT": Ins_STRI2INT(order),
                        "WRITE": Ins_WRITE(order),
                        "READ": Ins_READ(order),
                        "CONCAT": Ins_CONCAT(order),
                        "STRLEN": Ins_STRLEN(order),
                        "GETCHAR": Ins_GETCHAR(order),
                        "SETCHAR": Ins_SETCHAR(order),
                        "TYPE": Ins_TYPE(order),
                        "DPRINT": Ins_DPRINT(order),
                        "BREAK": Ins_BREAK(order),
                        "PUSHS": Ins_PUSHS(order),
                        "POPS": Ins_POPS(order),
                        "CALL": Ins_CALL(order),
                        "RETURN": Ins_RETURN(order)}

        if opcode not in instructions:
            self.raiseError(32, "Unknown operation code {0}, exiting...".format(opcode))

        return instructions[opcode]

    def addToList(self, instruction=None):
        """Adds instruction to the list of instructions"""
        if instruction is None:
            self.raiseError(99, "Trying to add empty instruction, exiting...")

        self.instruction_list.append(instruction)

    def printInstructionList(self):
        for ins in self.instruction_list:
            ins.printInstruction()

    def getInsFromList(self,order):
        for ins in self.instruction_list:
            if ins.order == order:
                return ins
        return -1

    def loadFromXML(self, file):
        """Loads XML from specified file and fills the instruction list"""
        tree = ET.parse(file)
        root = tree.getroot()

        if root.attrib["language"].lower() != "ippcode18":
            self.raiseError(52, "Program language is not IPPcode18, exiting...")

        for instruct in root:
            # Generate instruction and save it in i
            ins = self.generateInstruction(instruct.attrib["opcode"], instruct.attrib["order"])

            for arg in instruct:
                op = Operand(arg.attrib["type"], arg.text)
                ins.addOperand(op)

            self.addToList(ins)

    def interpret(self):
        self.instructionCounter = 1
        totalInstructions = len(self.instruction_list)+1

        self.buildLabels()

        while(self.instructionCounter != totalInstructions):
            #Load next instruction according to instructionCounter and execute it
            nextInstruction = self.getInsFromList(self.instructionCounter)

            #If we got a label instruction, skip it
            if nextInstruction.opcode == "LABEL":
                self.instructionCounter = self.instructionCounter + 1
                continue

            nextInstruction.execute()

            #Increment the instruction counter
            self.instructionCounter = self.instructionCounter + 1

    def buildLabels(self):
        for instruction in self.instruction_list:
            if instruction.opcode == "LABEL":
                instruction.execute()
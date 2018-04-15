import xml.etree.ElementTree as ET

class Instruction:
    """Class representing an instruction"""

    def __init__(self, order):
        self.order = int(order)
        self.ops_list = list()
        self.opcode = None
        self.interpreter = Interpreter.getInstance()

    def addOperand(self, operand=None):
        if operand is None:
            # TODO: Better error handling
            print("Trying to add empty operand, exiting...")
            exit(99)

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
        print("Instruction {0} executing, order is {1}".format(self.opcode,self.order))


class Ins_POPFRAME(Instruction):
    """POPFRAME instruction"""

    def __init__(self, order):
        super(Ins_POPFRAME, self).__init__(order)
        self.opcode = "POPFRAME"

    def execute(self):
        self.printExecuting()
        #self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        self.interpreter.popFrame()

class Ins_PUSHFRAME(Instruction):
    """PUSHFRAME instruction"""

    def __init__(self, order):
        super(Ins_PUSHFRAME, self).__init__(order)
        self.opcode = "PUSHFRAME"

    def execute(self):
        self.printExecuting()
        #self.check() TODO: Perform a check of operands (number of arguments, type etc...)
        self.interpreter.pushFrame()

class Ins_CREATEFRAME(Instruction):
    """CREATEFRAME instruction"""

    def __init__(self, order):
        super(Ins_CREATEFRAME, self).__init__(order)
        self.opcode = "CREATEFRAME"

    def execute(self):
        self.printExecuting()
        #self.check() TODO: Perform a check of operands (number of arguments, type etc...)
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
            # TODO: Better error handling
            print("Variable already exists in frame {0}, exiting...".format(frame))
            exit(54)

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
        var1.value = var2.getValue()
        var1.var_type = var2.var_type

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

class Operand:
    """Class representing single operand of an instruction"""

    def __init__(self, v_type, value):
        self.v_type = v_type
        self.value = value

    def check(self):
        """Checks if the operand is valid"""
        # TODO: Alot of checking to do here
        if self.v_type == "int":
            self.value = int(self.value)
            pass
        elif self.v_type == "bool":
            pass
        elif self.v_type == "string":
            pass
        elif self.v_type == "label":
            pass
        elif self.v_type == "type":
            pass
        elif self.v_type == "var":
            pass
        else:
            # TODO: Better error handling
            print("Non-existing type, exiting...")
            exit(53)

    def toVar(self):
        self.check()
        if self.v_type == "var":
            split = self.value.split("@")
            frame = split[0]
            name = split[1]

            #Get variable from specified frame
            var = Interpreter.getInstance().getVarFromFrame(frame, name)
            if var == -1:
                # TODO: Better error handling
                print("Variable does not exists in frame {0}, exiting...".format(frame))
                exit(54)
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

    def isVar(self):
        if self.v_type == "var":
            return True
        return False

    def isInt(self):
        if self.v_type == "int":
            return True
        return False

    def isBool(self):
        if self.v_type == "bool":
            return True
        return False

    def isString(self):
        if self.v_type == "string":
            return True
        return False

    def isLabel(self):
        if self.v_type == "label":
            return True
        return False

    def isType(self):
        if self.v_type == "type":
            return True
        return False

class Variable:
    """Class representing single variable to be stored in a frame"""

    def __init__(self, name, value=None, var_type=None):
        self.name = name
        self.value = value
        self.var_type = var_type

    def getValue(self):
        if self.value is None:
            # TODO: Better error handling
            print("Trying to access uninitialize variable, exiting...")
            exit(56)
        return self.value

    def printVar(self):
        print("Variable '{0}' has value '{1}' and type '{2}'".format(self.name,self.value,self.var_type))

class Frame:
    """Class representing a single frame"""

    def __init__(self):
        self.content = list()

    def addVar(self, var=None):
        if var is None:
            # TODO: Better error handling
            print("Trying to add empty variable, exiting...")
            exit(99)
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

        self.callStack = list() #Holds instruction number to return to on RETURN instruction
        self.frameStack = list() #Stack of frames

        self.localFrame = None #Local frame reference
        self.tempFrame = None #Temporary frame reference
        self.globalFrame = Frame() #Global frame reference

        self.loadFromXML(file)

    def getLocalFrame(self):
        if self.localFrame is None:
            # TODO: Better error handling
            print("No local frame, exiting...")
            exit(55)
        return self.localFrame

    def getTempFrame(self):
        if self.tempFrame is None:
            # TODO: Better error handling
            print("No temporary frame, exiting...")
            exit(55)
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
            # TODO: Better error handling
            print("No temporary frame, exiting...")
            exit(55)

        self.frameStack.append(self.tempFrame) #Push tempFrame to stack
        self.refreshLocalFrame() #Set new local frame
        self.tempFrame = None #Deinitialize tempFrame

    def popFrame(self):
        if self.localFrame is None:
            # TODO: Better error handling
            print("No local frame, exiting...")
            exit(55)

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
            print("Label {0} already defined, exiting...".format(label))
            exit(52)

        #Seems fine, add to the label list
        self.label_list.append({label: order})

    def jumpToLabel(self, label):
        label_dict = self.findLabel(label)
        if (label_dict == -1):
            print("Label {0} is not defined, exiting...".format(label))
            exit(52)

        #Set the instruction counter to the label position
        #print("Jumping to instruction number {0}".format(label_dict[label]+1))
        self.instructionCounter = label_dict[label]


    def findLabel(self, label):
        """Finds specified label in list, if the label is undefined it returns -1"""
        for d in self.label_list:
            if label in d:
                return d
        return -1


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
                        "IDIV": Ins_IDIV(order)}

        if opcode not in instructions:
            # TODO: Better error handling
            print("Unknown operation code {0}, exiting...".format(opcode))
            exit(32)

        return instructions[opcode]

    def addToList(self, instruction=None):
        """Adds instruction to the list of instructions"""
        if instruction is None:
            # TODO: Better error handling
            print("Trying to add empty instruction, exiting...")
            exit(99)

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

        # TODO: Check if root language is IPPcode18
        # print(root.attrib)

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

        while(self.instructionCounter != totalInstructions):
            #Load next instruction according to instructionCounter and execute it
            nextInstruction = self.getInsFromList(self.instructionCounter)
            nextInstruction.execute()

            #Increment the instruction counter
            self.instructionCounter = self.instructionCounter + 1

    def start(self):
        for instruction in self.instruction_list:
            instruction.execute()
import sys

def RemoveSpaces(x):
    if (x != " ") or (x != ", "):
        return x

def RemoveCommas(x):
    if x[-1] == ",":
        return x[ : len(x) - 1]
    else:
        return x

def CheckLiteral(element):
    if element[ : 2] == "='":
        return True
    else:
        return False

def CheckSymbol(Elements):
    global SymbolTable, Opcodes

    if (len(Elements) > 1) and ([Elements[-1], None, None, "Variable"] not in SymbolTable) and (Elements[-1] != "CLA") and (Elements[-2] not in ["BRP", "BRN", "BRZ"]) and (Elements[-1][ : 2] != "='") and (Elements[-1][ : 3] != "REG") and (not Elements[-1].isnumeric()):
        return True
    else:
        return False

def CheckLabel(Elements):
    global SymbolTable, Opcodes

    if (len(Elements) >= 2) and (Elements[1] in Opcodes):
        if Elements[0] not in SymbolTable:
            return True
    else:
        return False

Opcodes = ["CLA", "LAC", "SAC", "ADD", "SUB", "BRZ", "BRN", "BRP", "INP", "DSP", "MUL", "DIV", "STP", "DATA", "START"]
AssemblyOpcodes = {"CLA" : "0000", "LAC" : "0001", "SAC" : "0010", "ADD" : "0011", "SUB" : "0100", "BRZ" : "0101","BRN" : "0110",
                   "BRP" : "0111", "INP" : "1000", "DSP" : "1001", "MUL" : "1010", "DIV" : "1011", "STP" : "1100"}
SymbolTable = []
LiteralTable = []
Variables = []
Declarations = []
AssemblyCode = []
location_counter = 0
stop_found = False
end_found = False

file = open("Assembly Code Input.txt", "rt")

# ERROR 1 : Checking for missing START statement
for line in file:
    # Checking for comments
    if line[ : 2] != "//":
        if line.strip() != "START":
            print("STARTError : 'START' statement is missing. " + "( Line " + str(location_counter) + " )")
            sys.exit(0)
        else:
            file.seek(0, 0)
            break

# First Pass
for line in file:
    # Checking for comments
    if line[ : 2] != "//":
        Elements = line.strip().split(" ")
        Elements = list(filter(RemoveSpaces, Elements))
        Elements = list(map(RemoveCommas, Elements))

        # Removing comments
        for i in range(len(Elements)):
            if Elements[i][ : 2] == "//":
                Elements = Elements[ : i]
                break

        # ERROR 2 : Checking for too many operands
        # If the instruction doesn't contain a Label
        if (len(Elements) >= 3) and (Elements[0] in Opcodes):
            print("TooManyOperandsError : Too many operands used for the '" + Elements[0] + "' assembly opcode. " + "( Line " + str(location_counter) + " )")
            sys.exit(0)
        # If the instruction contains a Label
        elif (len(Elements) >= 4) and (Elements[1] in Opcodes):
            print("TooManyOperandsError : Too many operands used for the '" + Elements[1] + "' assembly opcode. " + "( Line " + str(location_counter) + " )")
            sys.exit(0)

        # ERROR 3 : Checking for less operands
        # If the instruction doesn't contain a Label
        if (len(Elements) == 1) and (Elements[0] in ["LAC", "SAC", "ADD", "SUB", "BRZ", "BRN", "BRP", "INP", "DSP", "MUL", "DIV"]):
            print("LessOperandsError : Less operands used for the '" + Elements[0] + "' assembly opcode. " + "( Line " + str(location_counter) + " )")
            sys.exit(0)
        # If the instruction contains a Label
        elif (len(Elements) == 2) and (Elements[1] in ["LAC", "SAC", "ADD", "SUB", "BRZ", "BRN", "BRP", "INP", "DSP", "MUL", "DIV"]):
            print("LessOperandsError : Less operands used for the '" + Elements[1] + "' assembly opcode. " + "( Line " + str(location_counter) + " )")
            sys.exit(0)

        # ERROR 4 : Checking for invalid opcodes
        if stop_found is False:
            if len(Elements) == 3:
                # If the instruction contains a Label
                if Elements[1] not in Opcodes:
                    print("InvalidOpcodeError : '" + Elements[1] + "' is an invalid opcode. " + "( Line " + str(location_counter) + " )")
                    sys.exit(0)
            if (len(Elements) == 2) and (Elements[1] == "CLA"):
                pass
            elif len(Elements) == 2:
                # If the instruction doesn't contain a Label
                if Elements[0] not in Opcodes:
                    print("InvalidOpcodeError : '" + Elements[0] + "' is an invalid opcode. " + "( Line " + str(location_counter) + " )")
                    sys.exit(0)

        # Check for STP
        if (len(Elements) == 3) and (Elements[1] == "DATA"):
            stop_found = True

        # Check for END
        if (len(Elements) == 1) and (Elements[0] == "END"):
            end_found = True

            for i in range(len(LiteralTable)):
                if LiteralTable[i][1] == -1:
                    LiteralTable[i][1] = location_counter
                    location_counter += 1

            break

        if not stop_found:
            # Check for Literal
            for x in Elements:
                if CheckLiteral(x):
                    LiteralTable.append([x, -1])

            # Check for Labels
            if CheckLabel(Elements):
                SymbolTable.append([Elements[0], location_counter, None, "Label"])

            # Check for Symbols
            if CheckSymbol(Elements):
                SymbolTable.append([Elements[-1], None, None, "Variable"])
        elif stop_found:
            if (Elements[0] != "STP") and (Elements[0] != "END"):
                # ERROR 5 : Checking for multiple definations
                if Elements[0] not in Variables:
                    Variables.append(Elements[0])
                    Declarations.append((Elements[0], Elements[2]))
                else:
                    print("DefinationError : Variable '" + Elements[0] + "' defined multiple times. " + "( Line " + str(location_counter) + " )")
                    sys.exit(0)

                # ERROR 6 : Checking for redundant declarations
                if [Elements[0], None, None, "Variable"] not in SymbolTable:
                    print("RedundantDeclarationError : " + Elements[0] + " declared but not used.")
                    sys.exit(0)
                location = SymbolTable.index([Elements[0], None, None, "Variable"])
                SymbolTable[location][1] = location_counter
                SymbolTable[location][2] = Elements[2]

        location_counter += 1

# ERROR 7 : Checking for missing END statement
if end_found is False:
    print("ENDError : 'END' statement is missing." + "( Line " + str(location_counter) + " )")
    sys.exit(0)

# ERROR 8 : Checking for undefined variables
for x in SymbolTable:
    if x[1] is None and x[3] == "Variable":
        print("UndefinedVariableError : Variable '" + x[0] + "' not defined.")
        sys.exit(0)

# Printing Tables after First Pass
print(">>> Opcode Table <<<\n")
print("ASSEMBLY OPCODE     OPCODE")
print("--------------------------")

for key in AssemblyOpcodes:
    print(key.ljust(20) + AssemblyOpcodes[key].ljust(6))

print("--------------------------")
print("\n>>> Literal Table <<<\n")
print("LITERAL     ADDRESS")
print("-------------------")

for i in LiteralTable:
    print(i[0].ljust(12) + str(i[1]).ljust(7))

print("-------------------")
print("\n>>> Symbol Table <<<\n")
print("SYMBOL          ADDRESS     VALUE     TYPE")
print("----------------------------------------------")

for i in SymbolTable:
    print(i[0].ljust(16) + str(i[1]).ljust(12) + str(i[2]).ljust(10) + i[3].ljust(10))

print("----------------------------------------------")
print("\n>>> Data Table <<<\n")
print("VARIABLES     VALUE")
print("-------------------")

for i in Declarations:
    print(i[0].ljust(14) + str(i[1]).ljust(10))

print("-------------------\n")

# Second Pass
file.seek(0, 0)

print(">>> MACHINE CODE <<<\n")

for line in file:
    # Checking for comments
    if line[ : 2] != "//":
        Elements = line.strip().split(" ")
        Elements = list(filter(RemoveSpaces, Elements))
        Elements = list(map(RemoveCommas, Elements))
        s = ""

        # Removing comments
        for i in range(len(Elements)):
            if Elements[i][ : 2] == "//":
                Elements = Elements[ : i]
                break

        # To terminate machine code conversion
        if (len(Elements) == 3) and (Elements[1] == "DATA"):
            break

        if Elements[0] == "STP":
            AssemblyCode.append("00 "+ AssemblyOpcodes["STP"] + " 00 00 00")
            print("00 " + AssemblyOpcodes["STP"] + " 00 00 00")
        # If the CLA opcode has a Label before it
        elif (len(Elements) == 2) and (Elements[1] == "CLA"):
            for i in range(len(SymbolTable)):
                if Elements[0] == SymbolTable[i][0]:
                    AssemblyCode.append(str(SymbolTable[i][1]).rjust(2, "0") + " " + AssemblyOpcodes["CLA"] + " 00 00 00")
                    print(str(SymbolTable[i][1]).rjust(2, "0") + " "+ AssemblyOpcodes["CLA"] + " 00 00 00")
        elif Elements[0] != "START":
            if (len(Elements) == 1) and (Elements[0] == "CLA"):
                AssemblyCode.append("00 " + AssemblyOpcodes["CLA"] + " 00 00 00")
                print("00 " + AssemblyOpcodes["CLA"] + " 00 00 00")
            # If there is no Label
            elif (len(Elements) == 2) and (Elements[1] != "CLA"):
                print("00 " + AssemblyOpcodes[Elements[0]], end = " ")
                s = "00 " + AssemblyOpcodes[Elements[0]] + " "

                # Dealing with Literals
                if CheckLiteral(Elements[1]):
                    for i in range(len(LiteralTable)):
                        if LiteralTable[i][0] == Elements[1]:
                            AssemblyCode.append(s + "00 00 " + str(LiteralTable[i][1]).rjust(2, "0"))
                            print("00 00 " + str(LiteralTable[i][1]).rjust(2, "0"))
                # Dealing with Lables (BRP, BRZ, BRN)
                elif Elements[0] in ["BRP", "BRN", "BRZ"]:
                    for i in range(len(SymbolTable)):
                        if SymbolTable[i][0] == Elements[1]:
                            AssemblyCode.append(s + str(SymbolTable[i][1]).rjust(2, "0") + " 00 00")
                            print(str(SymbolTable[i][1]).rjust(2, "0") + " 00 00")
                # Dealing with Registers
                elif Elements[1][ : 3] == "REG":
                    AssemblyCode.append(s + "00 " + Elements[1][-1].rjust(2, "0") + " 00")
                    print("00 " + Elements[1][-1].rjust(2, "0") + " 00")
                # Dealing with Variables
                else:
                    for i in range(len(SymbolTable)):
                        if SymbolTable[i][0] == Elements[1]:
                            AssemblyCode.append(s + "00 00 " + str(SymbolTable[i][1]).rjust(2, "0"))
                            print("00 00 " + str(SymbolTable[i][1]).rjust(2, "0"))
            # If the instruction conatins a Label
            elif len(Elements) == 3:
                for i in range(len(SymbolTable)):
                        if SymbolTable[i][0] == Elements[0]:
                            print(str(SymbolTable[i][1]).rjust(2, "0") + " " + AssemblyOpcodes[Elements[1]], end = " ")
                            s = str(SymbolTable[i][1]).rjust(2, "0") + " " + AssemblyOpcodes[Elements[1]] + " "

                # Dealing with Literals
                if CheckLiteral(Elements[2]):
                    for i in range(len(LiteralTable)):
                        if LiteralTable[i][0] == Elements[2]:
                            AssemblyCode.append(s + "00 00 " + str(LiteralTable[i][1]).rjust(2, "0"))
                            print("00 00 " + str(LiteralTable[i][1]).rjust(2, "0"))
                # Dealing with Lables (BRP, BRZ, BRN)
                elif Elements[1] in ["BRP", "BRN", "BRZ"]:
                    for i in range(len(SymbolTable)):
                        if SymbolTable[i][0] == Elements[2]:
                            AssemblyCode.append(s + str(SymbolTable[i][1]).rjust(2, "0") + " 00 00")
                            print(str(SymbolTable[i][1]).rjust(2, "0") + " 00 00")
                # Dealing with Registers
                elif Elements[2][ : 3] == "REG":
                    AssemblyCode.append(s + "00 " + Elements[2][-1].rjust(2, "0") + " 00")
                    print("00 " + Elements[2][-1].rjust(2, "0") + " 00")
                # Dealing with Variables
                else:
                    for i in range(len(SymbolTable)):
                        if SymbolTable[i][0] == Elements[2]:
                            AssemblyCode.append(s + "00 00 " + str(SymbolTable[i][1]).rjust(2, "0"))
                            print("00 00 " + str(SymbolTable[i][1]).rjust(2, "0"))

file.close()

file = open("Machine Code.txt", "x")

file.write("------------\nMACHINE CODE\n------------\n\n")

for x in AssemblyCode:
    file.write(x + "\n")

file.close()

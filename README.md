# Two-Pass-Assembler

A Python program that replicates a Two Pass Assembler. A Two-Pass Assembler performs two passes over the assembly language source code. In the First Pass, it iterates over all the lines and creates few essential tables, namely, Symbol Table, Literal Table, and Data Table. In the Second Pass, the Assembler translates the assembly code to machine language code.

The Two-Pass Assembler outputs an Opcode Table, a Symbol Table, a Literal Table, a Data Table, and the Machine Code for the input Assembly Code. It will also create a text file by the name of “Machine Code.txt” that consists of the machine language code for the input assembly language code.

* A `Symbol Table` includes all the variables and labels used in the assembly source code, their values (`None` for labels), their types (`Label` or “Variable”), and their addresses.
* A `Literal Table` consists of all the literals used in the assembly source code and their respective address.
* A `Data Table` consists of all the declared variables and the values assigned to them.
* An `Opcode Table` includes all the valid assembly opcodes and their respective machine opcodes. 

| S. NO | OPCODES | MEANING                                                                               | ASSEMBLY OPCODES |
|-------|---------|---------------------------------------------------------------------------------------|------------------|
| 1     | 0000    | Clear accumulator                                                                     | CLA              |
| 2     | 0001    | Load into accumulator from address                                                    | LAC              |
| 3     | 0010    | Store accumulator contents into the address                                           | SAC              |
| 4     | 0011    | Add address contents to accumulator contents                                          | ADD              |
| 5     | 0100    | Subtract address contents from accumulator contents                                   | SUB              |
| 6     | 0101    | Subtract address contents from accumulator contents                                   | BRZ              |
| 7     | 0110    | Branch to address if accumulator contains a negative value                            | BRN              |
| 8     | 0111    | Branch to address if accumulator contains a positive value                            | BRP              |
| 9     | 1000    | Read from the terminal and put in the address                                         | INP              |
| 10    | 1001    | Display value in the address on terminal                                              | DSP              |
| 11    | 1010    | Multiply accumulator and address contents                                             | MUL              |
| 12    | 1011    | Divide accumulator contents by address content. The quotient in R1 and remainder in R2| DIV              |
| 13    | 1100    | Stop execution                                                                        | STP              |

## Errors

The Two-Pass Assembler comprises an error reporting feature. If any error is found in the input assembly code, the Assembler outputs it in the console. The Assembler will output the error and end the program.

The Assembler can hunt for the following errors:
* `STARTError` : If the START statement is missing.
* `TooManyOperandsError` : If the number of operands provided for an 
opcode exceeds the required number of operands.
* `LessOperandsError` : If the number of operands provided for an 
opcode is less than the required number of operands.
* `InvalidOpcodeError` : If an invalid opcode is used in the assembly 
language code.
* `DefinationError` : If a variable is defined multiple times.
* `UndefinedVariableError` : If a variable is used in the program but not 
defined.
* `ENDError` : If the END statement is missing.
* `RedundantDeclarationError` : If a variable is declared but not used 
anywhere in the program.

## Example

To test the Two-Pass Assembler, do as follows - 
* Create a file by the name `Assembly Code Input.txt`.
* Add the following Machine code the the file.
* Run the `Assembler.py`.

```
            START
// Comment Number One
// Comment Number Two
LoopOne     CLA
            LAC   A
            ADD   ='1'
            SUB   ='35'
Loop        BRP   Subtraction       // Comment Number Three
Subtraction SUB   ='5'
            ADD   B                 // Comment Number Four
            MUL   C
            SUB   D
            MUL   ='600'
            BRZ   Zero              // Comment Number Five
Division    DIV   E
            CLA
            LAC   REG1
            BRP   Positive
Zero        SAC   X
            DSP   X
            STP
Positive    CLA
            DSP   REG1
            DSP   REG2
        A   DATA 250
        B   DATA 125
        C   DATA 90
        D   DATA 88
        E   DATA 5
        X   DATA 0
            END
```

In the first pass, the Two-Pass Assembler will create various tables, namely, Symbol Table, Literal Table, Data Table, and Opcode Table, and display them in the console.

In the second pass, with the help of these tables, the assembly code will be converted into the machine code. The Two-Pass Assembler will not only output the machine code in the console but also create a text file that has the machine code.

## Assumptions

The following are the assumptions taken under consideration while making this Two-Pass Assembler.
* The Assembly Language code always starts with a START statement, ends with the END statement, and the initial value of the location counter is always zero.
* All the operands are declared at the end of the assembly instructions, sequentially and in the order of their appearance in the code.
* There should be no Macros and Procs in the assembly language code.
* Literals are of the format `=’x’`, where `x` is a numeric value. For example, `=’1’`, `=’45’`, `=’12345’`, etc.
* The programming language used for making this Two-Pass Assembler is python.

# Compilers

## Typical compilation statement

`g++ -std=c++11 -g ./main.cpp -o ../bin/main`

`-g for debug (also -p for profile)`

## What is a compiler?

A compiler is a software tool that translates high-level programming code written in a human-readable language (such as C++, Java, Python, etc.) into low-level machine code, or bytecode, that can be executed by a computer's CPU (Central Processing Unit). The process of translation performed by a compiler is known as compilation.

## Here's how a compiler typically works

### Parsing

The compiler first reads the source code written by the programmer and parses it to understand its structure and syntax. This involves breaking down the code into smaller elements, such as keywords, identifiers, operators, and symbols.

### Semantic Analysis

After parsing, the compiler performs semantic analysis to ensure that the code adheres to the rules and constraints of the programming language. This includes type checking, variable declarations, function definitions, and other language-specific rules.

### Intermediate Representation

Many compilers generate an intermediate representation (IR) of the code after parsing and semantic analysis. The IR is a platform-independent representation of the code that simplifies further optimization and code generation.

### Optimization

Compilers often perform various optimization techniques to improve the efficiency and performance of the generated code. These optimizations may include dead code elimination, constant folding, loop unrolling, and inlining of functions.

### Code Generation

Finally, the compiler translates the optimized code into the target machine's specific instructions or bytecode. This process involves mapping high-level constructs to their corresponding low-level instructions, such as assembly language or bytecode.

### Output

The compiled code is typically stored in an executable file or object file, depending on the compiler and the target platform. This file can then be executed by the computer's operating system or further linked with other object files to create a complete executable program.

Compilers play a crucial role in the software development process, enabling programmers to write code in high-level languages while ensuring that it can be efficiently executed on a computer. They are essential tools for translating abstract programming concepts into instructions that a computer can understand and execute.

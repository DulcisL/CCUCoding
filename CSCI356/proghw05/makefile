# Compiler
CC = gcc -std=c99

# Target executable name
TARGET = 

# Source file(s) and object file(s)
SRCS = 
OBJS = $(SRCS:.c=.o)

# Default rule to build the target
$(TARGET): $(OBJS)
	$(CC) -o $(TARGET) $(OBJS) -I.

# Clean rule to remove generated files
clean:
	rm -f $(TARGET) $(OBJS) *.logs *tmp

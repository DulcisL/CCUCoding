# Compiler
CC = gcc -std=c99

# Target executable name
TARGET = war

# Source file(s) and object file(s)
SRCS = war_networked.c
OBJS = $(SRCS:.c=.o)

# Default rule to build the target
$(TARGET): $(OBJS)
	$(CC) -o $(TARGET) $(OBJS) -I.

# Clean rule to remove generated files
clean:
	rm -f $(TARGET) $(OBJS) *.logs *tmp *.s

CC      = gcc
CFLAGS  = -Wall -Wextra -std=c99
TARGETS = make-2d stencil-2d print-2d
OBJS    = utilities.o

all: $(TARGETS)

utilities.o: utilities.c utilities.h
	$(CC) $(CFLAGS) -c utilities.c

make-2d: make-2d.c
	$(CC) $(CFLAGS) -o $@ make-2d.c

stencil-2d: stencil-2d.c $(OBJS) timer.h
	$(CC) $(CFLAGS) -o $@ stencil-2d.c $(OBJS)

print-2d: print-2d.c
	$(CC) $(CFLAGS) -o $@ print-2d.c

clean:
	rm -f $(TARGETS) *.o

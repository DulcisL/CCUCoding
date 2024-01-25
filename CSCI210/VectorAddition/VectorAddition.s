.set noreorder

# this is what we need to do
#  int A[] = {1,2,3,4};
#  int B[] = {5,6,7,8};
#  int C[4];
#  int i; int dp = 0;
#  for(i=0; i<4; i++) {
#    C[i]=A[i]+B[i];
#    
#  } 

.global _start
_start:

# use t0 as the base address of A
la $t0, A

# use t1 as the base address of B
la $t1, B

# use t2 as the base address of C
la $t2, C

# initialize any variables you need here
#i
li $t3, 0

#dp
li $t4, 0

# outside of the loop

FOR:	# write a loop here

	#Check conditions
	addi $t7,$zero, 4
	beq $t3, $t7, END

		#Get address
		sll $t7, $t3,2
		add $t5, $t0, $t7
		add $t6, $t1, $t7
		
		lw $t5, 0($t5)
		lw $t6, 0($t6)
		#add A[i] + B[i]
		add $t5, $t5, $t6

		#store in C[i]
		add $t6, $t2, $t7
		sw $t5, 0($t6)

		#iterate i
		addi $t3, $t3, 1

		#jump to loop
		j FOR


# end the program
END:
	j END


.data
A: .word 1,2,3,4
B: .word 5,6,7,8
C: .word 0,0,0,0

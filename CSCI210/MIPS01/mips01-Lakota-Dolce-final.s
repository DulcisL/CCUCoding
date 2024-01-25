# Tell assembler to not insert instructions to fill branch delay slots.
# This is necessary when branch delay slots are disabled.
.set noreorder

.global _start
_start:

	# need to call sort on A , pass it the size of A (6 elements)

	# pass the pass the parameters to sort() which expects to have the values in a0 and a1 respectively.
	la $sp, 0x7ffffffc #Set the stack pointer to match book
	la $a0, A	# load A for access later
	li $a1, 6	# the length of the array

	jal print_array     #Call the print_array function
	jal descending_sort #Call the descending_sort()
	jal print_array		#Call the print_array function
	
END:
	li $v0, 10
	syscall


descending_sort:    
		 addi $sp,$sp, -24      # make room on stack for 5 registers
		 sw $a1, 20($sp)		# save a1 on stack
         sw $ra, 16($sp)        # save $ra on stack
         sw $s3,12($sp)         # save $s3 on stack
         sw $s2, 8($sp)         # save $s2 on stack
         sw $s1, 4($sp)         # save $s1 on stack
         sw $s0, 0($sp)         # save $s0 on stack
         
         move $s2, $a0           # save $a0 into $s2
         move $s3, $a1           # save $a1 into $s3
         move $s0, $zero         # i = 0
for1tst: 
		 slt  $t0, $s0, $s3      # $t0 = 0 if $s0 ≥ $s3 (i ≥ n)
         beq  $t0, $zero, exit1  # go to exit1 if $s0 ≥ $s3 (i ≥ n)
         addi $s1, $s0, -1       # j = i – 1
for2tst: 
		 slti $t0, $s1, 0        # $t0 = 1 if $s1 < 0 (j < 0)
         bne  $t0, $zero, exit2  # go to exit2 if $s1 < 0 (j < 0)
         sll  $t1, $s1, 2        # $t1 = j * 4
         add  $t2, $s2, $t1      # $t2 = v + (j * 4)
         lw   $t3, 0($t2)        # $t3 = v[j]
         lw   $t4, 4($t2)        # $t4 = v[j + 1]
         slt  $t0, $t4, $t3      # $t0 = 0 if $t4 ≥ $t3
         bgt  $t0, $zero, exit2  # go to exit2 if $t4 < $t3
         move $a0, $s2           # 1st param of swap is v (old $a0)
         move $a1, $s1           # 2nd param of swap is j
         jal  swap               # call swap procedure
         addi $s1, $s1, -1       # j –= 1
         j    for2tst            # jump to test of inner loop
		 
		 exit2:   addi $s0, $s0, 1        # i += 1
         	j    for1tst         # jump to test of outer loop
		 
		 exit1: 
		 	lw $s0, 0($sp)  	   # restore $s0 from stack
         	lw $s1, 4($sp)         # restore $s1 from stack
         	lw $s2, 8($sp)         # restore $s2 from stack
         	lw $s3,12($sp)         # restore $s3 from stack
         	lw $ra,16($sp)         # restore $ra from stack
			lw $a1,20($sp)		   # restore $a1 from stack
         	addi $sp, $sp, 24      # restore stack pointer
         	jr $ra                 # return to calling routine

swap: sll $t1, $a1, 2   # $t1 = k * 4
      add $t1, $a0, $t1 # $t1 = v+(k*4)
                        #   (address of v[k])
      lw $t0, 0($t1)    # $t0 (temp) = v[k]
      lw $t2, 4($t1)    # $t2 = v[k+1]
      sw $t2, 0($t1)    # v[k] = $t2 (v[k+1])
      sw $t0, 4($t1)    # v[k+1] = $t0 (temp)
      jr $ra            # return to calling routine
	  
print_array:
	addi $sp, $sp, -4	
	sw $a0, 0($sp)		#Save the $a0 to the stack to be restored later
	
	move $t0, $a1	#Get length of array
	move $t1, $a0	#Get the array address
	addi $t2, $t1, 0
	
	li $v0, 4		#syscall print string
	li $a0, str		#load string 
	syscall			#print the string
	
	loop:#make a loop
		beq $t1, $t2, no_comma  #check to see if you should print a comma
		li $v0, 4	   #syscall print ,
		li $a0, str_comma
		syscall
		
		no_comma:
			li $v0, 1		   #syscall 1 print number
			lw $a0, 0($t1)	   #put the number in $a0
			syscall	
		
		
		addi $t1, 4		   #increment to next array value
		addi $t0, -1	   #reduce length by 1
		bne $t0, $zero, loop #if $t0 != 0 continue loop
						   #Else print new line and exit
		li $v0, 4
		li $a0, str_close
		syscall
		
		li $v0, 11
		li $a0, '\n'
		syscall			   #Print a new line
		
	lw $a0, 0($sp)         # restore $a0 from stack
	addi $sp, $sp, 4	   #restore stack pointer
	
	jr $ra


.data
A: .word 2, 4, 3, 1, 9, 7
str: .string "array = {"
str_close: .string "}"
str_comma: .string ","
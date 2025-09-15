# PSEUDOCODE — Step-by-step for each program

## make-matrix.c
```
parse_args()
if making matrix:
    read rows, cols, output filename
    allocate double[rows*cols]
    fill array with chosen pattern or RNG
    write header (rows, cols)
    write data block in row-major order
else if making vector:
    read length, output filename
    allocate double[length]
    fill with pattern/RNG
    write header (length)
    write data block
```

## print-matrix.c
```
parse_args()
open file and read first two integers
if it's a vector format:
    length = header[0]
    print length, then up to K elements
else:  # matrix
    rows=header[0], cols=header[1]
    print dims and optionally a small preview by rows/cols
```

## matrix-vector-multiply.c (serial)
```
parse_args() -> matrix_file, vector_file, output_file
start timer 'read'
A = read_matrix(matrix_file)      # rows, cols, data[]
x = read_vector(vector_file)      # len, data[]
assert A.cols == x.len
stop timer 'read'

start timer 'compute'
allocate y[rows]
for i in 0..rows-1:
    acc = 0
    for j in 0..cols-1:
        acc += A[i*cols + j] * x[j]
    y[i] = acc
stop timer 'compute'

start timer 'write'
write_vector(output_file, y, rows)
stop timer 'write'

print timers for read, compute, write
```

## mpi-matrix-vector-multiply.c
```
MPI_Init
rank, size = MPI_Comm_rank/size

if rank == 0:
    read header (rows, cols) from matrix_file
broadcast rows, cols to all ranks
compute local_rows for each rank (block distribution)

# Everyone needs the vector x fully:
if rank == 0: read vector (len=cols) from file
broadcast x to all ranks

# Distribute matrix rows:
if rank == 0:
    for r in 0..size-1:
        send A[rows_for_r] to rank r (or keep local slice)
else:
    recv local matrix block

# Local compute
for i in 0..local_rows-1:
    y_local[i] = dot( A_local[i,*], x )

# Gather results
if rank == 0:
    allocate y[rows]
gatherv(y_local -> y on rank 0)

if rank == 0:
    write y to output file
MPI_Finalize
```

## Python tests
```
- generate small deterministic inputs with make-matrix
- call serial or MPI binary via subprocess
- read output and verify against numpy.dot(A, x)
- assert timings are present and files exist
```

/*
params
pth-stencil-2d -n <iters> -I <in.raw> -o <out.raw> [-s <stack.raw>] -t <threads>
  -n ITERS      Number of iterations (time steps)
  -I FILE       Input grid (.raw) header+data (int rows, int cols, doubles)
  -o FILE       Output final grid (.raw) header+data
  -s FILE       (optional) Raw stack output file (writes header + all frames)
  -t NTHREADS   Number of pthreads (>=1)
  -h

*/
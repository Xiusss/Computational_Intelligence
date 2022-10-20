# Labs
These are my Labs for the course "Computational Intelligence" at Politecnico di Torino in collaboration with @vmask25 e @Saccuz.

## Lab1
Given a number $N$ and some lists of integers $P = (L_0, L_1, L_2, ..., L_n)$, determine, if possible, $S = (L_{s_0}, L_{s_1}, L_{s_2}, ..., L_{s_n})$, such that each number between $0$ and $N-1$ appears in at least one list, and that the total numbers of elements in all $L_{s_i}$ is minimum.


Test cases and optimal solutions:(found/not found, solution, # element repetitions)

N = 5:
Processed nodes with BF: 2625
Number of elements in solution:5


N = 10:
Processed nodes with BF: 20875
Number of elements in solution:10

N = 20:
Processed nodes with BF: 331211
Number of elements in solution:23

With N = 50 and N=100 computing time explodes.

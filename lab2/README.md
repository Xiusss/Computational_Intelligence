# Lab 2: Set Covering through a genetic algorithm

## Task
Given a number $N$ and some lists of integers $P = (L_0, L_1, L_2, ..., L_n)$ determine, if possible, $S = (L_{s_0}, L_{s_1}, L_{s_2}, ..., L_{s_n})$ such that each number between $0$ and $N-1$ appears in at least one list and that the total numbers of elements in all $L_{s_i}$ is minimum.

## Development

### 1. Prove that a solution exists

Through the analysis of the results obtained in the first lab, we know that a solution exists. We are committed in finding the optimal one with a wide problem space, focusing on performance with N=1000 and N=5000. 

### 2. Find the Optimal Solution
To find the optimal solution, we opted for a genetic algorithm where we represent each genome as a bitmap of 0's and only one "1" randomly chosen.  
With a tournament_size=2, using a lambda+mi strategy we substitute a part of the population in order to keep the fittest at that iteration. The cross-over strategy we use composes the result picking a slice of random dimension from each of the parents.   
To determine the fitness of a potential solution we maximize the covered numbers and minimize the amount of collisions(maximizing -collisions).
To prevent elitarism we apply a double mutation with a rate of 30%.
With a reasonable time we achieve good solutions for high values of N.

Comparing to lab1, we succedeed in calculating the solution for $N$ bigger than 20 reaching N=5000.

Theese are our results with 1000 generations:

| $N$  | Collisions | Weight |
|------|------------|--------|
| 5    | 0          | 5      |
| 10   | 0          | 10     |
| 50   | 43         | 93     |
| 100  | 99         | 199    |
| 500  | 1003       | 1503   |
| 1000 | 2804       | 3804   |
| 2000 | 7900       | 9900   |
| 5000 | 24945      | 29945  |
## Contributors

- [Marco Sacchet](https://github.com/saccuz)
- [Simone Mascali](https://github.com/vmask25)

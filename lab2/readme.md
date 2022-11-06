# Lab 2
## Team: 
- Lorenzo Radaele s301165
- Fabio Sofer s301195

## Description
We started from one-max script adding some functions and changing the fitness method.

As in the first lab we have considered both the cost of the current solution and its coverage to compute the fitness; also here we have used a multiplier factor with a sligthy different meaning, being able to prioritize the coverage percentage in respect to the number of repetitions
Furthermore we have added a penalty to the fitness score if the genome solution is not valid, this help us to find the best valid solutions without discarding possible paths that pass through non-valid solutions.

Each generation we have an high probability of mutating 5 times, still it must be noticed that also in the case two individuals are crossed-over the son is mutated one time.

## Results

| N       | Ls   | Fitness    | Bloat       | Time(# of fitness call) | K |
|------------|-----------|----------|----------|---------------|-------|
| 5         | 5 | 10 | 0% |    10000          | 3 |
| 10 |   10 | 20 | 10% |       20000        | 3 |
| 20 | 24 | 36| 20% |     100000        | 3 |
| 100  |  189 | 111 | 89% |   100000          | 3 |
| 500  | 1658| -158 | 231,6% |  100000            | 3 |
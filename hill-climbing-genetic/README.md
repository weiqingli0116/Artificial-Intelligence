# Hill-climbing and Genetic for Urban planning
## The problem
For this problem, I will use hill climbing and genetic algorithms to determine the ideal location of industry, commerce, and residential sections a city.  I will input a map with the following symbols:
* X:  former toxic waste site.  Industrial zones within 2 tiles take a penalty of -10.  Commercial and residential zones within 2 tiles take a penalty of -20.  You cannot build directly on a toxic waste site.
* S:  scenic view.  Residential zones with 2 tiles gain a bonus of 10 points.  If you wish, you can build on a scenic site but it destroys the view.  
* 0...9:  how difficult it is to build on that square.  You will receive a penalty of that many points to put anything on that square.  

sample:
1

1

1

X,1,2,4

3,4,S,3

6,0,2,3

The first three line is the number of Industrial tiles, commercial tiles and Residential tiles.

I will have to place industrial, residential, and commercial tiles on the terrain.  
* Industrial tiles benefit from being near other industry.  For each industrial tile within 2, there is a bonus of 3 points.
*	Commercial sites benefit from being near residential tiles.  For each residential tile within 
*	3 squares, there is a bonus of 5 points.  However, commercial sites do not like competition.  For each commercial site with 2 squares, there is a penalty of 5 points.
*	Residential sites do not like being near industrial sites.  For each industrial site within 3 squares there is a penalty of 5 points.  However, for each commercial site with 3 squares there is a bonus of 5 points.

Note that all distances uses the Manhattan distance approach. So distance is computed in terms of moves left/right and up/down, not diagonal movement.
Approaches

I will use hill climbing with restarts and genetic algorithms for this problem.  

## Hill Climbing 
Hill Climbing is heuristic search used for mathematical optimization problems in the field of Artificial Intelligence .

Given a large set of inputs and a good heuristic function, it tries to find a sufficiently good solution to the problem. This solution may not be the global optimal maximum.
![](https://i.stack.imgur.com/HISbC.png)
### Step
1. Compute cost of each possible move

      Remember, goal is to find a better state
  
      if a move is clearly worse, don’t need an exact count

2. Pick whichever move has the lowest possible cost
### Local Optimal Maximum
* Restart: Try again (and again, and again, and…)

* Sideways move: Don’t require moving towards the goal

### About This Problem
The heuristic function is the score of this map by the rule mentioned before.

When your hill climbing restarts, it may not modify the map! It can only change where it initially places the different zones to begin the hill climbing process.  

## Genetic Alogrithm
Genetic algorithms simulate the process of natural selection which means those species who can adapt to changes in their environment are able to survive and reproduce and go to next generation.
Combine elements of two solutions together to get a better one

### Elitism, Culling and Mutation
Elitism:

We could lose a near solution through random combination. Within elitism we will keep the best k% ones in our population.

Culling:

Remove weakest states from population. Within culling, we are more likely to get a higher score answer by combining two parents.

Mutation:

Randomly change some bits. To add more variety.

### Step
1. Start with k randomly generated states (population) 

2. Do until “done”

    1. Select k2<<k most fit states to be preserved (elitism)
  
    2. Remove weakest states from population (culling)
  
    3. Repeat 
  
        * Select two states semi-randomly
      
          * Weight towards states with better fitness
        
          * Think of fitness as opposite of heuristic function
        
        * Combine two states to generates two successors
      
        * Randomly change some bits in the states (mutation)

      Until population is full

### About this problem

In our genetic algorithm, the answer of the urban planning is stored as a list. In this list, there is the coordinates of industrial, commercial and residential places. These coordinates are stored in order of “industrial places, commercial places and residential places”. So, when giving the number of industrial, commercial and residential places, we could get the coordinates of these three kind of tiles.

1. Set population: we randomly produce N individuals as the population. N is the population size. In our program, we set N=250.

2. Elitism: Reserve the top 10% of the initial population into the new population based on the scores of these individuals.

3. Selection & Crossover: Keep selecting two parents at one time randomly from the initial population and make them cross-over until the number of reproducer reaches the size of the initial population.

4. Mutation: Set a mutation rate of 0.05. During the cross-over process, one point in the child would possibly mutate to a random point which is available on the map.

5. Culling: Put those children into the new population and combine with the reserved ones, which means that we now get a whole new population whose size is 1.1N. The new population contains the elite and the crossover result of the initial population. We now process the culling procedure where we find the 10% worst genes in the new group based on their scores and cull them.

6. After culling, put the processed population back to step one until we reach the termination criteria.

#### Selection and Crossover
For selection, in the original genetic program, we randomly choose two parents from the population with help of the sample function in Python. From the parents, we could get I1,C1,R1 for industrial tile lists, commercial tile lists and residential tile lists of parent1; I2,C2,R2 for those of parent2.

For crossover:

1. we randomly select the new industrial tiles from the union set of I1 and I2 and
named the new industrial tiles list as new_I. Same as industrial tiles, we could get
new commercial tiles list new_C and residential tiles list new_R.

2. Remove duplicates. There could be duplicates among new_I, new_C and new_R
which means it is possible that two buildings (e.g. industrial site and commercial site) would be built on the same tile. This kind of outcome is not qualified, so we have to remove all duplicates.

  1. Check all the coordinates in new_C. if a coordinate has shown in new_I, wewillrandomlychooseanewonein 𝐶1∪𝐶2 −(𝑛𝑒𝑤_𝐼∪𝑛𝑒𝑤_𝐶) when this set is not empty or randomly choose one in the available positions. Thus, the new point would be unique in the new_I + new_C.

  2. Check all the coordinates in new_R. in this time, the coordinates in new_R should not been in new_I and new_C. If there is one shown in it, we randomly choose a new one form 𝑅1 ∪ 𝑅2 − ( 𝑛𝑒𝑤_𝐼 ∪ 𝑛𝑒𝑤_𝐶 ∪ 𝑛𝑒𝑤_𝑅 ) if it is not empty or from available positions.
At this point, we complete the crossover and get children as new_I + new_C + new_R.

Also, we tired a new way of selection called roulette selection. In this time, the probability of each individual being selected is proportional to its fitness. In our case, the probability is proportional to its score.

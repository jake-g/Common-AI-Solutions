
[Source](http://homes.cs.washington.edu/~shapiro/EE562/hw1/index.html "Permalink to Artificial Intelligence for Engineers Autumn 2016")

# Artificial Intelligence for Engineers Autumn 2016

## Autumn 2016


### HW ASSIGNMENT 1 (Warmup): Monday, Oct 10th at 11:59 pm (15 pts)

Solve the Missionary-Cannibal Problem (with 3 missionaries and 3 cannibals) witha RECURSIVE DEPTH-FIRST SEARCH as follows:

Requirements

* You must use a recursive depth-first search. No frontier. Just simple recursion, up and down the search tree. It is usually called a backtracking search.
* No repeated states. When you reach a state for which there is an identical ancestor on the same path, the search backs up. For this, you will need to keep a stack of the path above the current state.
* Count how many states are searched to find each solution; there are four. For your counting keep track of 3 kinds of states you generate:
    * illegal states in which the cannibals eat the missionaries,
    * repeated states that are the same as an ancestor state on the same path,
    * total states searched (ie. all states except the illegal and repeated ones).
* You should use Python for this assignment. It is a Python warmup.
* Please comment each method, describing its purpose, arguments and return value.
* Please comment important sections of code; 'This is the main search', 'This checks for repeated states', etc.
* Your program should print out all paths it finds to the goal state and the three counts for each path.

Turn In: [here][2]

You should turn in the following:

* your well-commented code
* the solutions your program finds, each solution being an ordered list of states from initial state to goal state. Format as follows:

(3,3,L)(3,1,R)(3,2,L)...(0,0,R)

* The 3 counts: illegal count, repeat count, total count for each solution.

Evaluation:

* search works and produces correct solutions (10 pts)
* 3 counters work and counts are printed for each solution (3 pts)
* code is readable and well commented (2 pts)

LATE POLICY: Programs may be turned in until Wednesday night, October 12 at 11:59pm. 10% off for each day late.

CHEATING POLICY: All work on this assignment must be your own. You may discuss the assignment with other members of the class, but your code should not look like anyone else's code. Having the same code with different names for the variables doesn't work either. We check. Thanks.

[1]: http://homes.cs.washington.edu/cannibals.jpg
[2]: https://catalyst.uw.edu/collectit/dropbox/shapiro/38809

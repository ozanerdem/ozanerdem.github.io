---
layout: post
title:  "Introduction to Integer Programming with Cbc"
date:   2019-06-18 22:03:20 -0400
categories: jekyll update
mathjax: true
---

{% include mathjax.html %}


This series of posts will cover a brief introduction to
integer programming using the Cbc solver[^cbc]. Even though I have quite some experience in solvers for various computational problems, I have only recently started using Cbc, and I am far from being an expert on it. The following few posts will both be an introduction to integer programming for other people, and will also document my experience with Cbc.

These posts will refer to "integer programming", however most of the content would still
be applicable to "integer linear programming (ILP)", also known as "mixed
integer linear programming (MILP). The difference between the former and the
latter two is that integer programming admits only integer variables. This distinction does not change the
complexity of the problem, and the decision version of all are NP-complete.

## Basic definition

Integer programming is an optimization paradigm that aims to minimize/maximize a linear objective function over integer variables with respect to a set of linear constraints. In mathematical terms, that is:

$$
\textrm{minimize}\ G(x)
$$

subject to

$$
f_1(x) \\
f_2(x) \\
\ldots \\
f_n(x) \\
$$

where each $x$ is an integer, $$G(x)$$ is a linear function, and $$f_i(x)$$ are all linear
inequalities[^inequality]. In other terms, we want to optimize $$G(x)$$ while
satisfying all the constraints $$f_1(x), f_2(x), \ldots, f_n(x)$$ at the same
time. 

## Why do we care about integer programming?

In computer science, algorithms, methods, and paradigms have a
degree of usefulness in two dimensions:

* What can we solve with this tool? What are the problems that we can express
  in the language (or input) this tool, and what are the ones that we cannot?
* How efficient is this tool?

The questions regarding the first question can be answered by noting that integer programming is very useful for solving combinatorial optimization problems. Some examples are popular puzzles (like generalized versions of Sudoku, FreeCell, and even Candy Crush[^candycrushref]), various scheduling problems (job-shop scheduling, flow shop scheduling, multiprocessor scheduling), and interesting computer science problems with many practical applications (traveling salesperson problem, graph coloring, graph partitioning).

However, these examples by themselves do not give us the precise set of
problems we can express with integer programming. Luckily, complexity theory gives us some insight on the usefulness of this
paradigm (and similar NP-complete paradigms). If you are not interested in the
theory of integer programming, you can skip to the [next section](#an-example-problem) to see how
we can solve integer programming problems in practice.

### What can we solve with integer programming?
To discuss the set of problems we can solve with integer programming, let us first
consider the "decision version" of the integer programming problem:

**Decision Problem:** Given a constant $$ k $$, is the following set of constriants satisfiable?

$$
G(x) \leq k \\
f_1(x) \\
f_2(x) \\
\ldots \\
f_n(x) \\
$$

Note that, in some sense, this is equivalent to the optimization version: If you
are able to  solve the decision version for some $$k$$, you can increase $$k$$
one by one to find the maximum value. Conversely, if you are able to solve the
optimization version, you can also decide all the $$k$$ values the decision
version can satisfy.

To show the usefulness of integer programming, we will leverage a significant
result of Stephen Cook, known as Cook's Theorem[^cook], which states that the Boolean
satisfiability problem is NP-complete. In other terms, given any problem in the
NP complexity class we can express it as an instance of the Boolean satisfiability
problem, and solve it with a satisfiability solver.

In a similar fashion, we can show that given an integer programming solver, we
can use it to solve "any" instance of the Boolean satisfiability sroblem. If we
can show this, due to transitivity, it would mean that we can use an integer programming solver to
solve any problem in NP.

To show this, let us examine what the Boolean satisfiability problem is. It
asks for an assignment to Boolean variables that satisfy clauses $$ C_1,
C_2, \ldots, C_n$$ at the same time, where each clause is the "or" of variables $x$ or negations
of variables $$\neg x$$. We also denote a possibly negated variable a
"literal". Hence, a clause can be written as $$(l_1 \vee l_2 \vee \ldots \vee l_n)$$,
where $$ \vee $$ is the symbol for "or", and each $$l_i$$ is a literal.

To show that we can solve the satisfiability problem with an integer
programming solver, all we need to do is to show how we can model each clause
as a linear constraint over integers.

It turns out that this is pretty straightforward: Each Boolean variable $$x$$ in the
satisfiability problem will corresponding to an integer programming variable $$0 \leq x' \leq 1$$, each positive
literal $$x$$ corresponds to the variable $$ x' $$, and each negative literal
$$\neg x$$ corresponds to an expression $$ 1-x' $$. Let us denote this
linear term corresponding to literal $$l$$ to
$$term(l)$$. With all this machinery, we now can boil down each clause $$(l_1 \vee l_2 \vee \ldots \vee l_n)$$ as $$term(l_1) + term(l_2) + \ldots + term(l_n) \geq 1$$. It is easy to see that whenever the clause is satisfied the linear inequality is satisfied, and vice versa.

This concludes the our somewhat-informal proof that we can use an integer
programming solver to solve "any" problem in NP.

So far so good! The only missing piece of the puzzle is knowing what the NP complexity
class stands for. NP stands for "nondeterministic polynomial time", which is the set of decision problems that we can verify the
solutions in polynomial time[^npclass], and it covers all the polynomial problems, as well
as all the interesting NP-complete problems.
Of course, if you know a polynomial problem, you would
not use integer programming to solve it as it is too much big of a hammer,
however it is nice to know that it is possible to do so.

### How efficient is integer programming?

The short answer is: We do not know! To this date, we do not know of any
algorithms to solve integer programming problem in polynomial time, and this is
actually known as the "P versus NP problem" in computer science[^pvsnp]. If we follow the
reasoning in the previous subsection, we can make the following remarks:

* If there was an algorithm to solve the integer programming problem in
  polynomial time, we could solve all the instances of the Boolean
  satisfiability problem in polynomial time (with the conversion we did in the
  previous section).
* If we can solve the Boolean satisfiability problem in polynomial time, then
  we can solve all the problems in NP in polynomial time (according to Cook's
  Theorem).
* If we can solve all the problems in NP in polynomial time, that would be a
  proof of $$P=NP$$.

Even though we do not know whether we can solve the integer programming problem
in polynomial time, we know this: If you have a NP-complete problem at hand,
and if you think you can solve it very efficiently, then you should think twice: If
your method is fast indeed, you can solve any integer programming instance (or
Boolean satisfiability instance, or anything in NP) with that method, by
boiling down your problem to any of these. Given that there are hoards of
researchers working to improve solvers for these problems for decades, I would
consider giving these solvers a try.

Of course, this line of reasoning can break if we consider the following:
* When we convert problems to each other, we can introduce
  "inefficiencies". For instance, as we saw above, there is a very direct
  mapping from the Boolean satisfiability problem instances to integer
  programming instances. However, even though the converse is possible, it is
  not that straightforward and it will increase the number of variables and constraints in
  the problem.
* If you are a domain expert in your own problem, then you might very easily
  come up with useful heuristics that a generic integer programming solver might not
  come up with. Moreover, there is a good chance that your constraints have
  patterns, and you can come up with specialized data structures to hold them (rather than
  for instance, generic sparse matrices an integer programming solver would use).
  However, you should also consider the fact that your own domain expertise can
  be embedded in an integer programming solvers, which are very customizable in
  general.

Additionally, you also would not want to use an integer programming solver to
solve any problem that can be already solved with a polynomial algorithm. For
instance, an integer programming solver might take exponential time to solve
the shortest path problem, and it makes much more sense to use a polynomial
algorithm instead.

For these reasons, even if you are working on an NP-complete problem, it is very hard to know up front whether an integer programming solver will
be as fast as your custom method in practice. However, if your work requires
you to solve some NP-complete problem, you probably should know that
standard solvers for standard problems exist, and also how to make use of them
when needed.

## An example problem

Assume that you are the head of a production facility, and as the head one of
you many responsibilities is to maximize the revenue. For the sake of the
example, assume that you only get to decide how many units of "Good A" and
"Good B" you will produce. Assuming that you can sell the first one for 2
dollars, and the second one for 3 dollars, what you want to maximize is this
linear form:

$$
2A + 3B
$$

Of course, you also have some constraints, otherwise your revenue will be
unbounded! Assume that you have 10 resources of type $$X$$ and 14 resources of
type $$Y$$ that you use to produce these goods. You know that to produce each
Good A, you need 3 $$X$$s and a $$Y$$, and to produce each Good B, you need an
$$X$$ and 3 $$Y$$s. Hence, you needs to satisfy the following constraints:

$$
3A+B \leq 10 \\
A+3B \leq 14 \\
A \geq 0 \\
B \geq 0 
$$

where $$A$$ and $$B$$ are integers, as producing fractional numbers of goods
does not make much sense. Hence, this is an instance of the integer programming problem, we can use an integer
programming solver to optimize our revenue!

## Using Cbc

Cbc is an open-source integer programming solver, that can solve integer programs, as well as mixed integer linear programs. In the rest of this post, I
will demonstrate how to use Cbc for solving the toy problem above.


Installation of Cbc is pretty easy, it comes with a script called "coinbrew",
which fetches the sources and the dependencies automatically, and you can use
it to build and install the solver as well.

As also mentioned in the project readme, the following commands should handle all these steps for you:

```
/path/to/coinbrew fetch Cbc
/path/to/coinbrew build =Cbc --prefix=/dir/to/install --test
/path/to/coinbrew install Cbc
```

### Input format

We can view the set of constraints in the instance as a single equality in
matrix form: $$Ax \leq b$$, where $$A$$ is a matrix, $$x$$ is a variable vector,
and $$b$$ is a constant vector. Any integer programming solver would let us
specify $$A$$ and $$b$$ somehow, either explicitly or implicitly.

The primary input format to Cbc is MPS, which stands for "Mathematical
Programming System". This is quite an awkward format, as:
* It requires you to specify the constraints column by column. I find this very
  counter-intuitive, as I normally think of a problem as a set of constraints,
  which would be specified as row by row.
* The format has fixed column positions.

According to [Wikipedia](https://en.wikipedia.org/wiki/MPS_(format)), solvers seem to have extensions and lifted restrictions to the format. I am not sure whether Cbc supports any extensions, however what is below seems to work fine even though I did not put the columns in the fixed locations specified in the format:

```
NAME     EXAMPLE
ROWS
 N  COST
 L  C1
 L  C2
COLUMNS
 A  COST 2    C1   3
 A  C2   1
 B  COST 3    C1   1
 B  C2   3
RHS
 C1           10
 C2           14
BOUNDS
 LI BND1      A         0
 LI BND1      B         0
ENDATA
```

I will not go to the deep details of the format, however most of it should be
intuitive:
* There are 5 sections: NAME, ROWS, COLUMNS, RHS, and BOUNDS
* The ROWS section lists all the names of the rows (constraints), and the type
  of inequality:
  * N is for the objective function
  * L is a "less than or equal to" constraint
* Each line in the COLUMNS section starts with a column name (variable), and
  lists the coefficients 
* RHS section lists the right hand side of each constraint
* BOUNDS lists the bounds of each variable. LI stands for a lower bound for an
  integer variable, and actually if we leave out lower bounds than they are
  assumed to be zero in Cbc. However, I believe this is not guaranteed in every
  solver, hence I am being explicit.

Additionally, Cbc seems to support reading the Lp format, which is much more
intuitive. However, even though the C++ API handles it, looks like the
standalone executable does not seem to support it.

## Solving with Cbc

When Cbc is called with the following command:

```
cbc -direction=maximize -import example.mps -solve -solution solution.txt
```

we get the following output:

```
Option for direction changed from min!imize to max!imize
At line 1 NAME     EXAMPLE
At line 2 ROWS
At line 6 COLUMNS
At line 11 RHS
At line 14 BOUNDS
At line 17 ENDATA
Problem EXAMPLE has 2 rows, 2 columns and 4 elements
Coin0008I EXAMPLE read with 0 errors
Continuous objective value is 16 - 0.00 seconds
Cgl0004I processed model has 2 rows, 2 columns (2 integer (0 of which binary)) and 4 elements
Cutoff increment increased from 1e-05 to 0.9999
Cbc0012I Integer solution of -16 found by DiveCoefficient after 0 iterations and 0 nodes (0.00 seconds)
Cbc0001I Search completed - best objective -16, took 0 iterations and 0 nodes (0.00 seconds)
Cbc0035I Maximum depth 0, 0 variables fixed on reduced cost
Cuts at root node changed objective from -16 to -16
Probing was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
Gomory was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
Knapsack was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
Clique was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
MixedIntegerRounding2 was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
FlowCover was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
TwoMirCuts was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
ZeroHalf was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)

Result - Optimal solution found

Objective value:                16.00000000
Enumerated nodes:               0
Total iterations:               0
Time (CPU seconds):             0.01
Time (Wallclock seconds):       0.02

Total time (CPU seconds):       0.01   (Wallclock seconds):       0.02

```

Since this is a trivial instance, Cbc solved it without even doing any search!
This is due to the fact that the optimal solution to the problem is also a
solution to the linear programming relaxation of the instance, however I will
leave what that means to a later post.

In the output, we can see that the objective value is 16, which is the maximum
profit we can make under our constraints.

Moreover, if we peek at the generated file `solution.txt`, we see the
following:

```
Optimal - objective value 16.00000000
      0 A                      2                       2
      1 B                      4                       3
```

Even though I did not look up what each column means, the following is evident:
* First column shows the variable ids
* The second column shows the variable names
* The third column shows the values of the variables in the optimal solution
* The last column shows the coefficients of the variables in the objective
  function.

## Summary

In the following few posts, I will dive deeper into practicalities of Cbc, such
as modeling and solving problems using the C++ API, and customizing the behaviour of the solver. Hope you enjoyed
this post, and looking forward to hear any comments!

### Notes

[^candycrushref]: [Candy Crush is NP-hard](https://arxiv.org/abs/1403.1911)
[^inequality]: The definition can be extended to include equalities as well, as an equality can be written as two inequalities.
[^cook]: [Cook's Theorem](https://en.wikipedia.org/wiki/Cook%E2%80%93Levin_theorem)
[^cbc]: [COIN-OR Branch-and-Cut Solver](https://github.com/coin-or/Cbc)
[^pvsnp]: [P versus NP problem](https://en.wikipedia.org/wiki/P_versus_NP_problem)
[^npclass]: [NP complexity class](https://en.wikipedia.org/wiki/NP_(complexity))

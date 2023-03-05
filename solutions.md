<!---
Maryam: I've been compiling this on upmath.me, it will preview and allow for download.
-->

#### COSC-351 - HW 01 - Solving Wordle with Information Theory

[Wordle](https://en.wikipedia.org/wiki/Wordle) is a game that became very
popular in 2022, and is now [owned by the New York
Times](https://www.nytimes.com/games/wordle/index.html). If you are not familiar
with it, please see the [Wikipedia page](https://en.wikipedia.org/wiki/Wordle):
you got this far in this course, so understanding how Worlde works should be
very easy =).

In this assignment, we will develop a solver for Wordle that uses a strategy
grounded on the basic concepts of Information Theory, such as entropy and mutual
information.

##### Defining the random variables

Suppose to be at the start of a game of Wordle. We can define three random
variables:

* $$T$$, the unknown *target* word, which is distributed *uniformly* over a
    dictionary $$W$$ of possible five-letters words.[^1]
* $$G$$, our first guess, which also takes value over $$W$$, according to a
    distribution that we want to compute;
* $$P$$, the pattern of black, yellow, and green squares that result from our
    guess.

**Task 1:** Argue that $$T$$ and $$G$$ have *zero* mutual information, i.e.,
$$I[T;G] = 0$$.

**Task 2:** Argue that, conditioning on $$P$$, $$T$$ and $$G$$ have *positive*
conditional mutual information $$I[T;G \mid P] > 0$$.

**Task 3:** Argue that $$H[P \mid G,T] = 0$$.

[^1]: The assumption of uniformity greatly simplifies the analysis, but it is
  quite unrealistic: words are chosen according to some *interestingness
  criteria*, which may involve, e.g., their frequencies, or at least the
  frequencies of their characters in the English language.

##### The strategy to an optimal guess

Intuitively, our strategy should be to choose our guess from a distribution that
minimizes the expected size of the set of target words that are compatible with
the pattern resulting from our guess. The information-theoretic formalization is
that we want to choose a guess $$G \sim \pi$$ such that the resulting patter is
maximally informative w.r.t. the target. I.e., we want to solve the following
*optimization problem*:

$$ \text{Find the distribution}\ \pi\ \text{over}\ W\ \text{that maximizes}\ I[T;P \mid G].$$

**Task 4**: Argue that any optimal solution $$\pi'$$ to the above optimization
problem is also an optimal solution to the problem

$$\text{Find the distribution}\ \pi\ \text{over}\ W\ \text{that minimizes}\ H[T \mid G,P].$$

*Hint:* You want to expand $$I[T;P \mid G]$$, and show that some terms do not
depend on $$\pi$$, thus can be ignored.

If you think about it, the second optimization problem makes a lot of sense,
given what we know about conditional entropy: we want to minimize the leftover
uncertainty about the target.

**Task 5:** Show that we can rewrite $$H[T \mid G,P]$$ as

$$H[T \mid G,P] = \frac{1}{|W|} \sum_{g \in W} \pi(g) \alpha_g,$$

where $$\alpha_g$$ is a constant (dependent on $$g$$)), i.e., it does not depend on
$$\pi(g)$$.

*Hint:* to derive the expression for $$\alpha_g$$, use the assumption of
uniformity of $$T$$ over $$W$$. You will see that the expression for
$$\alpha_g$$ includes the number of words in $$W$$ that are compatible with the
pattern $$p$$ resulting from $$g$$.

##### Solving the optimization problem

The optimization problem we want to solve requires us to find the probability
distribution $$\pi$$ that minimizes

$$\frac{1}{|W|} \sum_{g \in W} \pi(g) \alpha_g.$$

In this expression, the $$\alpha_g$$'s are *known* (i.e., computable) constants,
while the $$\pi(g)$$'s are our *unknowns*, or *variables*. The above expression is
a *linear* function of $$\pi$$. We must not forget the constraints that $$\sum_{g
\in W} \pi(g) = 1$$,and that $$\pi(g) \ge 0$$, to ensure that our solution is a
probability distribution. Both these constraints are *linear* in the variables.
Thus, we need to solve a *linear* optimization problem.

We are in luck: solving linear optimization problem is very easy: there is
always at least one optimal solution $$\pi'$$ that would concentrate all the
probability mass on one $$g \in G$$. Formally, there is an optimal solution $$\pi'$$
is such that there exists a $$g_{\pi'} \in W$$ s.t. $$\pi'(g_{\pi'}) = 1$$, and
$$\pi(g) = 0$$ for any $$g \in W$$, $$g \neq g_{\pi'}$$.

**Task 6:** Argue that, if there are multiple $$g_1,g_2,\dotsc,g_k \in W$$ with
the same minimum value for $$\alpha_{g_1} = \alpha_{g_2} = \dotsb =
\alpha_{g_k}$$, then *any* distribution $$\pi$$ s.t. $$\sum_{i=1}^k \pi(g_i) =
1$$ and $$\pi(g_i) \ge 0$$ for $$i=1,\dotsc,k$$, is an optimal solution.

##### Guessing in the following rounds

After we select our first guess, we get a pattern back, and we can filter $$W$$ to
obtain the dictionary $$W'$$ of possible targets that are compatible with the
pattern. We can then repeat the analysis to select our next guess from $$W'$$, and
so on, until we guess correctly. The procedure is guaranteed to end because at
each step $$|W'| < |W|$$ as, at the very least, $$W'$$ does not contain our most
recent guess.

##### Implementation

**Task 7:** Implement a program `worldesolver` that takes two command line
arguments (in the following order):

1. `file`: a file with a list of five-letters words, one word per line;
2. `target`*: a word that is present in the file, representing the target.

Your program must then print on standard output, one per line, the sequence of
guesses it makes to guess `target*, together with the values of $$\alpha_g$$ for
each guess, and the obtained pattern, in the form

```
guess1, alpha_1, YBGYB
guess2, alpha_2, YYGGB
...
target, alpha_j, GGGGG
```

where, in the pattern, `Y` denotes a yellow square, `B` a black one, and `G` a
green one. *Extra credit*: colored square emojis in place of the letters.

<!-- Word list from https://github.com/tabatkins/wordle-list -->
An example `file` is attached below.

You can use any programming language you want, as long as it is Python or Java
=). If using Python, your program must be able to be called with `python
wordlesolver.py file target`. If using Java, it must run with `java Wordlesolver
file target`. If you *really* want to use a different programming language,
please ask Matteo first, *and* add instructions on how to compile/run your
program at the top of the `README` file included in your submission (see below).

I expect your program to behave "well" (i.e., print an informative error message
on standard error and exit) when the number of command line arguments is wrong,
or `file` does not exist or is malformed (e.g., contains words of length
different than five), or when `target` is not in `file`, or in any other case of
error.

**Hint**: the number of target words compatible with the pattern resulting from
a guess $$g$$ does not change from one round to the other, as long as $$g$$ is still
a possible target word.

**Hint**: when filtering $$W$$, first eliminate the words non compatible with the
green squares in the patterns, and then those among the leftovers that are not
compatible with the yellow squares. Don't forget to filter out your guess.

##### Submission

Your submission *must* include:

1. a *PDF* with your answers for Tasks 1-6;
2. all the files needed to run your progam;
3. A `README` plaintext file that explains how your program selects the
   distribution $$\pi$$ when there are multiple words with the same minimum
   value for $$\alpha_g$$ (see Task 6).

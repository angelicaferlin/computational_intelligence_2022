# Lab 3

## Colaborators and co-authors
I colaborated and wrote the code together with Leonor Gomes, Mathias Schmekel, Karl Wennerström and Erik Bengtsson.

## Other sources
[Code from professor](https://github.com/squillero/computational-intelligence/blob/master/2022-23/lab3_nim.ipynb)

### Evolutionary algorithm
Talking to people. Cowrote with Karl
# Evolved Strategy

An individual is looking like below. Parameters:
- a, c, e, g and i = how many elems should be left in a row after the agent has played (if the parameter > elem in row -> take one elem),
- b, d, f, h = indicates which row to pick from, depending on rule.

```
indv = {'Rule1': a, 'Rule2': [b, c], 'Rule3': [d, e], 'Rule4': [f, g], 'Rule5': [h, i], 'fitness': k}
```

The rules whoose parameters are evolved:
1. If only one active row left on the board, leave a number of parameters.
2. If even amount of active rows are left in the board and only one of the rows has more than 1 elem:
    - if b = 0, take from row with only one elem
    - if b = 1, leave c amounts of elem in row.
3. If even amount of active rows are left in the board and more than 2 rows have multiple elems:
    - if d = 0, leave e elem in the longest row
    - if d = 1, leave e elem in the shortest row
4. If odd amount of active rows are left in the board and only one of the rows has more than 1 elem:
    - if f = 0, take from row with only one elem
    - if f = 1, leave g amounts of elem in row.
5. If odd amount of active rows are left in the board and more than 2 rows have multiple elems:
    - if h = 0, leave i elem in the longest row
    - if h = 1, leave i elem in the shortest row <br />


onerow-stategy: only one row - leave x
2 rows: 1 rad = 1 element. ta x element från den andra raden
2 rows: both has more than 1 element - take random
else: take random random. 




### Min-Max
For the min-max a lot of code and inspiration was taken from this article
[Min-max article with code example](https://realpython.com/python-minimax-nim/)

### Q-learning
[Article](https://andrewrowell.blog/2020/05/19/q-learning-nim-with-python/)
[Example of code](https://github.com/abelmariam/nimPy/blob/master/Agent.py)
[Wiki: q-learning](https://en.wikipedia.org/wiki/Q-learning)
[Master theisis on q-learning and nim](https://www.csc.kth.se/utbildning/kth/kurser/DD143X/dkand11/Group6Lars/erik.jarleberg.report.pdf)
[Book on RL](http://incompleteideas.net/book/RLbook2020.pdf)

## Task 3.1 - Agent with fixed rules


## Task 3.2 - Evolved Agent

## Task 3.3 - Min-max Agent

## Task 3.4 - Agent using reinforcement learning with Q-learning and off-policy mechanism
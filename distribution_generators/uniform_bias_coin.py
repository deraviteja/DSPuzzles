#
# Q: Let's say every time you toss a coin, you are actually provided a coin
#   with a bias 'p' sampled from a uniform distribution.
#   What is the probability that you toss 2 heads consecutively?

import random
import numpy as np

number_of_experiments = 100000
not_two_heads = 0

for trial in range(0, number_of_experiments):

    coin_head_bias = random.uniform(0, 1)

    my_tosses = np.random.choice(['head', 'tail'], replace=True, size=2, p=[coin_head_bias, 1- coin_head_bias])

    for my_toss in my_tosses:

        if my_toss != 'head':

            not_two_heads = not_two_heads + 1

            break

print((number_of_experiments - not_two_heads) / number_of_experiments)



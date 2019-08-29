#
# Q: Let's say every time you toss a coin, you are actually provided a coin
#   with a bias 'p' sampled from a uniform distribution.
#   What is the probability that you toss 2 heads consecutively?

import random
import numpy as np
from scipy.stats import beta
from scipy.stats import halfnorm

number_of_experiments = 100000
not_two_heads = 0

for trial in range(0, number_of_experiments):

    coin_head_bias = random.uniform(0, 1)

    my_tosses = np.random.choice(['head', 'tail'], replace=True, size=2, p=[coin_head_bias, 1- coin_head_bias])

    for my_toss in my_tosses:

        if my_toss != 'head':

            not_two_heads = not_two_heads + 1

            break
actual_output = round(1.0/3, 4)
estimated_output = round((number_of_experiments - not_two_heads) / number_of_experiments, 4)
print("Probability of two heads occurring on a coin with bias lying on a uniform distribution is,")

print("\t Actual output ::", actual_output)
print("\t Estimated output ::", estimated_output)
print("\t Error ::", round(100*abs(actual_output - estimated_output)/ actual_output, 2), "%")


#
# Q: Let's modify the above experiment to sample bias from a generic continuous pdf function f,
#   with compact support [0,1]
#   We now sample from f, which gives us the bias of the coin to be used to toss twice
#   What is the probability that you toss 2 heads consecutively?

# A: integral( x^2 f(x) dx) over 0 to 1
# --> Let's say we sample 'x', 'x' gets sampled with a probability of f(x)dx ..
# --> The probability of 2 heads is now x^2, given x was sampled
# --> The cumulative probability is the summation, which becomes an integral since f is continuous valued
# --> Also, note that this is simply the expectation of x^2 over f
#   Let's simulate and find out!

#       We will use beta distributions to test this out! They qualify our requirements
#            (continuous with compact support [0,1])

parameter_alpha = round(halfnorm.rvs(size=1)[0], 4)
# I hate hard coded values, so this is how get around that OCD
#   generate random assignments with a normal distribution or half of it

parameter_beta = round(halfnorm.rvs(size=1)[0], 4)

my_beta_distribution = beta(a=parameter_alpha, b=parameter_beta)

not_two_heads = 0

for trial in range(0, number_of_experiments):

    coin_head_bias = my_beta_distribution.rvs(size=1)[0]

    my_tosses = np.random.choice(['head', 'tail'], replace=True, size=2, p=[coin_head_bias, 1 - coin_head_bias])

    for my_toss in my_tosses:

        if my_toss != 'head':

            not_two_heads = not_two_heads + 1

            break

print("Probability of two heads occurring on a coin \n \t with bias lying on a beta"
      " distribution with (a,b) : %s is, " %((parameter_alpha, parameter_beta), ))

actual_output = round(my_beta_distribution.expect(func=lambda key: key*key), 4)
estimated_output = round((number_of_experiments - not_two_heads) / number_of_experiments, 4)

print("\t Actual output ::", actual_output)
print("\t Estimated output ::", estimated_output)
print("\t Error ::", round(100*abs(actual_output - estimated_output)/actual_output, 2), "%")

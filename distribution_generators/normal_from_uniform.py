import numpy as np
from matplotlib import pyplot
from scipy.stats import norm
import math

#   let's generate a uniform distribution ~ U[a,b]

uniform_a = 0
uniform_b = 1
uniform_number_generator = lambda size: np.random.uniform(low=uniform_a, high=uniform_b, size=size)

#   let's verify by creating histograms

sample_data = uniform_number_generator(size=10000)


#       create 'n' bins around the generated data

number_of_bins = 10

pyplot.hist(sample_data, bins=number_of_bins)

pyplot.title("A given uniform number generator")

pyplot.grid()

pyplot.show()

normal_cdf = norm.cdf


def find_where_cdf_is(x=0, my_cdf=norm.cdf):

    start_value = 0
    end_value = 1

    while math.fabs(start_value - end_value) > 1.0E-5:

        if x < my_cdf(start_value):

            new_start_value = start_value - 2 * (end_value - start_value)

            end_value = start_value

            start_value = new_start_value

        elif my_cdf(start_value) < x < my_cdf(end_value):

            start_value = start_value + (end_value - start_value)/2.0

        else:

            new_end_value = end_value + 2 * (end_value - start_value)

            start_value = end_value

            end_value = new_end_value

    print x, start_value

    return start_value


generated_normal_samples = [find_where_cdf_is(x=data) for data in sample_data]

# print generated_normal_samples

pyplot.hist(generated_normal_samples, bins=number_of_bins)

pyplot.grid()

pyplot.title("A generated normal distribution")

pyplot.show()





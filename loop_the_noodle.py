"""
Q: You have 100 noodles in your soup bowl.
Being blindfolded, you are told to take two ends of some noodles
(each end of any noodle has the same probability of being chosen)
in your bowl and connect them.
You continue until there are no free ends.
The number of loops formed by the noodles this way is stochastic. Calculate the expected number of circles.

"""
import random

total_number_of_noodles = 75


def noodle_string_for_other_end(noodle_id_string):

    noodle_string, noodle_id, noodle_end = noodle_id_string.split('_')
    noodle_end = int(noodle_end)
    noodle_other_end = 1 - noodle_end

    return noodle_string + "_" + noodle_id + "_" + str(noodle_other_end)


noodle_ends = list()

for noodle in range(total_number_of_noodles):

    noodle_end_1 = "Noodle_" + str(noodle) + "_0" # using 0/1 for easy bit flip later
    noodle_end_2 = "Noodle_" + str(noodle) + "_1"

    noodle_ends.append(noodle_end_1)
    noodle_ends.append(noodle_end_2)

assert len(noodle_ends) == 2*total_number_of_noodles

noodle_ends_list = noodle_ends.copy()

number_of_experiments = 100000

samples = []

for experiment in range(number_of_experiments):

    noodle_ends = noodle_ends_list.copy()

    random.shuffle(noodle_ends)

    total_loops = 0

    next_noodle_id = total_number_of_noodles

    while noodle_ends:

        end_one = random.choice(noodle_ends)
        noodle_ends.remove(end_one)

        end_two = random.choice(noodle_ends)
        noodle_ends.remove(end_two)

        noodle_string, noodle_id_1, noodle_end_1 = end_one.split('_')
        noodle_id_1, noodle_end_1 = int(noodle_id_1), int(noodle_end_1)

        noodle_string, noodle_id_2, noodle_end_2 = end_two.split('_')
        noodle_id_2, noodle_end_2 = int(noodle_id_2), int(noodle_end_2)

        if noodle_id_2 == noodle_id_1:

            total_loops = total_loops + 1

            # print("New loop formed {}".format(noodle_id_1))

        else:

            noodle_ends.remove(noodle_string_for_other_end(end_one))

            noodle_ends.remove(noodle_string_for_other_end(end_two))

            new_noodle_end = noodle_string + "_" + str(next_noodle_id) + "_0"

            noodle_ends.append(new_noodle_end)

            noodle_ends.append(noodle_string_for_other_end(new_noodle_end))

            next_noodle_id += 1

            # print("New noodle formed {}".format(next_noodle_id))

    print("\n Experiment id {},  Total loops formed :: {} \n ".format(experiment, total_loops))

    samples.append(total_loops)

print("Sample average : {}".format(sum(samples) / len(samples)))

print("Expected value {}".format(sum([1/((2*k) + 1) for k in range(total_number_of_noodles)])))

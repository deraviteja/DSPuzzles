import random


def xor_data_generator(size=100):
    """

    :param size: number of data points to generate
    :return:
    """

    input_data_choices = [(0, 1), (1, 1), (1, 0), (0, 0)]

    random_input_data_points = [random.choice(input_data_choices) for i in range(size)]

    input_choice_count = dict()

    for input_data_choice in input_data_choices:

        input_choice_count[input_data_choice] = 0

    for data_point in random_input_data_points:

        input_choice_count[data_point] += 1

    for input_data_choice in input_data_choices:

        print("For data ", input_data_choice,
              " samples are ",
              input_choice_count[input_data_choice])

    result_data_point = [data_point[0]*(1 - 2*data_point[1]) + data_point[1] for data_point in random_input_data_points]

    return random_input_data_points, result_data_point


if __name__ == "__main__":

    xor_input, xor_output = xor_data_generator(size=100)

    for x, y in zip(xor_input, xor_output):

        print(x, y)



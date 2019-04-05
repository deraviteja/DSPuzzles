#   Function that takes in 3 data points and
#       outputs a generator function that generates points from the triangle, uniformly

import collections
import numpy as np
import math
import warnings

two_D_coordinate = collections.namedtuple("TWO_D_Coordinate", ['x','y'])


def triangle_generator(point1, point2, point3, size=100):
    """

    :param point1:
    :param point2:
    :param point3:
    :param size:
    :return: points "uniformly" sampled from the triangle formed  by the given points
    """
    point1 = two_D_coordinate(*point1)
    point2 = two_D_coordinate(*point2)
    point3 = two_D_coordinate(*point3)

    if point1 == point2 == point3:

        warnings.warn("All 3 points are the same.")

        return [(point1.x, point1.y) for i in range(0, size)]

    elif point1 == point2:

        warnings.warn("Two of the 3 points are same, so sampling from the straight line.")

        return straight_line_uniform_generator(point1=point1, point2=point3, size=size)

    elif point1 == point3:

        warnings.warn("Two of the 3 points are same, so sampling from the straight line.")

        return straight_line_uniform_generator(point1=point2, point2=point3, size=size)

    elif point2 == point3:

        warnings.warn("Two of the 3 points are same, so sampling from the straight line.")

        return straight_line_uniform_generator(point1=point1, point2=point3, size=size)

    elif collinear_points(point1, point2, point3):

        warnings.warn("The points are collinear, so sampling from the straight line.")

        if point1.x == point2.x:

            if (point3.y - point1.y) * 1.0 / (point2.y - point1.y) > 1:

                return straight_line_uniform_generator(point1=point1, point2=point3, size=size)

            elif (point3.y - point1.y) * 1.0 / (point2.y - point1.y) < 0:

                return straight_line_uniform_generator(point1=point2, point2=point3, size=size)

            else:
                return straight_line_uniform_generator(point1=point1, point2=point2, size=size)

        elif (point3.x - point1.x)*1.0 / (point2.x - point1.x) > 1:

            return straight_line_uniform_generator(point1=point1, point2=point3, size=size)

        elif (point3.x - point1.x)*1.0 / (point2.x - point1.x) < 0:

            return straight_line_uniform_generator(point1=point2, point2=point3, size=size)

        else:

            return straight_line_uniform_generator(point1=point1, point2=point2, size=size)

    else:

        def line_to_sample(u):
            return [
                two_D_coordinate(x=(point1.x + u*(point3.x - point1.x)), y=(point1.y + u*(point3.y - point1.y))),
                two_D_coordinate(x=(point1.x + u * (point2.x - point1.x)), y=(point1.y + u * (point2.y - point1.y)))
            ]

        return [straight_line_uniform_generator(*line_to_sample(u=math.sqrt(u_sample)), size=1)[0]
                for u_sample in np.random.uniform(low=0, high=1, size=size)]


def collinear_points(point1, point2, point3):
    """

    :param point1:
    :param point2:
    :param point3:
    :return: Custom function to determine if the points input are collinear
    """

    if isinstance(point1, two_D_coordinate) and isinstance(point2, two_D_coordinate)\
            and isinstance(point3, two_D_coordinate):

        if point1.y == point2.y == point3.y or point1.x == point2.x == point3.x:

            return True

        elif point1.y == point2.y or point2.y == point3.y or point3.y == point1.y:

            return False

        elif point1.x == point2.x or point2.x == point3.x or point3.x == point1.x:

            return False

        elif (point1.x - point2.x) * 1.0 / (point1.y - point2.y) == (point3.x - point2.x) * 1.0 / (point3.y - point2.y):

            return True

        else:

            return False


def straight_line_uniform_generator(point1, point2, size=100):

    """

    :param point1:
    :param point2:
    :param size:
    :return: function that returns samples "uniformly" from a straight line
    """

    return [(point1.x + u*(point2.x-point1.x), point1.y + u*(point2.y-point1.y))
            for u in np.random.uniform(low=0, high=1, size=size)]


if __name__ == "__main__":

    from matplotlib import pyplot

    triangle_coordinates = [(0, 0), (1, 0), (0, 3)]

    sampled_coordinates = triangle_generator(*triangle_coordinates, size=10000)

    pyplot.plot([sampled_coordinate[0] for sampled_coordinate in sampled_coordinates],
                [sampled_coordinate[1] for sampled_coordinate in sampled_coordinates],'bo')

    min_x = 1.01 * min([triangle_coordinate[0] for triangle_coordinate in triangle_coordinates]) - \
            0.01 * max([triangle_coordinate[0] for triangle_coordinate in triangle_coordinates])

    max_x = 1.01 * max([triangle_coordinate[0] for triangle_coordinate in triangle_coordinates]) - \
            0.01 * min([triangle_coordinate[0] for triangle_coordinate in triangle_coordinates])

    min_y = 1.01 * min([triangle_coordinate[1] for triangle_coordinate in triangle_coordinates]) - \
            0.01 * max([triangle_coordinate[1] for triangle_coordinate in triangle_coordinates])

    max_y = 1.01 * max([triangle_coordinate[1] for triangle_coordinate in triangle_coordinates]) - \
            0.01 * min([triangle_coordinate[1] for triangle_coordinate in triangle_coordinates])

    pyplot.xlim([min_x, max_x])

    pyplot.ylim([min_y, max_y])

    pyplot.grid()

    pyplot.show()

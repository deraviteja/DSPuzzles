import collections
from distribution_generators.triangular_data_generator import triangle_generator

two_D_coordinate = collections.namedtuple("TWO_D_Coordinate", ['x','y'])


def line_equation(p1, p2):
    """

    :param p1:
    :param p2:
    :return:
    """
    if not isinstance(p1, two_D_coordinate) or not isinstance(p2, two_D_coordinate):

        raise Exception("Not of coordinate type")

    def line(x, y):

        return x - p2.x if p1.x == p2.x else (y - p1.y) - ((p1.y - p2.y) / float(p1.x - p2.x)) * (x - p1.x)

    return line


class Triangle(object):

    __area__ = -1

    def __init__(self, p1=(0, 0), p2=(1, 1), p3=(0.2, 1.4)):
        """

        :param p1: point in a triangle
        :param p2: point in a triangle
        :param p3: point in a triangle
        """
        # print(p1, p2, p3)

        self.point1 = two_D_coordinate(x=p1[0], y=p1[1])
        self.point2 = two_D_coordinate(x=p2[0], y=p2[1])
        self.point3 = two_D_coordinate(x=p3[0], y=p3[1])

        self.__area__ = self.area()

        self.side_1 = line_equation(p1=self.point2, p2=self.point3)
        self.side_2 = line_equation(p1=self.point3, p2=self.point1)
        self.side_3 = line_equation(p1=self.point1, p2=self.point2)

    def area(self):

        if self.__area__ < 0:
            """
            Compute the area
            """

            self.__area__ = 0.5 * (- self.point2.y * self.point3.x +
                                   self.point1.y * (-self.point2.x + self.point3.x) +
                                   self.point1.x * (self.point2.y - self.point3.y) + self.point2.x * self.point3.y)

        return self.__area__

    def generate_uniform_samples(self, size=1000):

        return triangle_generator(self.point1, self.point2, self.point3, size=size)

    def is_in_triangle(self, p1=(1, 2)):
        """

        :param p1:
        :return:
        """

        if self.side_1(*self.point1) * self.side_1(*p1) < 0 or \
                self.side_2(*self.point2) * self.side_2(*p1) < 0 or \
                self.side_3(*self.point3) * self.side_3(*p1) < 0:

            return False

        else:

            return True

from utils.geometry import Triangle, two_D_coordinate
import numpy as np
from matplotlib import pyplot
from distribution_generators.triangular_data_generator import straight_line_uniform_generator
from tensorflow import keras
import tensorflow as tf
from random import shuffle


def single_sample(): return np.random.uniform(low=0, high=10, size=1)[0]


def data_generator(size_0=10000, size_1=10000, polygon=Triangle()):

    sampled_triangle_coordinates = polygon.generate_uniform_samples(size=size_1)

    triangle_x = [triangle_coordinate[0] for triangle_coordinate in sampled_triangle_coordinates]

    triangle_y = [triangle_coordinate[1] for triangle_coordinate in sampled_triangle_coordinates]

    min_x, max_x, min_y, max_y = min(triangle_x), max(triangle_x), min(triangle_y), max(triangle_y)

    def bounding_square(size):
        return [(x[0], y[1]) for x, y in
                zip(straight_line_uniform_generator(two_D_coordinate(1.1 * min_x - 0.1 * max_x, 0),
                                                    two_D_coordinate(1.1 * max_x - 0.1 * min_x, 0), size=size),
                    straight_line_uniform_generator(two_D_coordinate(0, 1.1 * min_y - 0.1 * max_y),
                                                    two_D_coordinate(0, 1.1 * max_y - 0.1 * min_y), size=size))]

    sample_square_coordinates = bounding_square(size=size_0)

    sample_square_coordinates = [square_coordinate for square_coordinate in sample_square_coordinates if
                                 not sample_triangle.is_in_triangle(p1=square_coordinate)]

    not_triangle_x = [not_triangle_coordinate[0] for not_triangle_coordinate in sample_square_coordinates]
    not_triangle_y = [not_triangle_coordinate[1] for not_triangle_coordinate in sample_square_coordinates]

    triangle_data = [(x, y, 1) for x, y in zip(triangle_x, triangle_y)]

    not_triangle_data = [(x, y, 0) for x, y in zip(not_triangle_x, not_triangle_y)]

    generated_data = triangle_data + not_triangle_data

    shuffle(generated_data)

    return generated_data


triangle_coordinates = [(single_sample(), single_sample()),
                        (single_sample(), single_sample()),
                        (single_sample(), single_sample())]

sample_triangle = Triangle(*triangle_coordinates)

training_data = data_generator(size_0=10000, size_1=5000, polygon=sample_triangle)

pyplot.plot([data[0] for data in training_data if data[2] == 0],
            [data[1] for data in training_data if data[2] == 0], 'bo', c='0.8')

pyplot.plot([data[0] for data in training_data if data[2] == 1],
            [data[1] for data in training_data if data[2] == 1], 'bo', c='0.2')

pyplot.xlim([min([data[0] for data in training_data]), max([data[0] for data in training_data])])
pyplot.ylim([min([data[1] for data in training_data]), max([data[1] for data in training_data])])

pyplot.grid()
pyplot.show()

testing_data = data_generator(size_0=2000, size_1=2000, polygon=sample_triangle)

pyplot.plot([data[0] for data in testing_data if data[2] == 0],
            [data[1] for data in testing_data if data[2] == 0], 'bo', c='0.8')

pyplot.plot([data[0] for data in testing_data if data[2] == 1],
            [data[1] for data in testing_data if data[2] == 1], 'bo', c='0.2')

pyplot.xlim([min([data[0] for data in testing_data]), max([data[0] for data in testing_data])])
pyplot.ylim([min([data[1] for data in testing_data]), max([data[1] for data in testing_data])])

pyplot.grid()
pyplot.show()

class_0 = sum([1 for data in training_data if data[2] == 0])
class_1 = sum([1 for data in training_data if data[2] == 1])
base_accuracy = float(class_0) / float(class_0 + class_1)

base_accuracy = base_accuracy if base_accuracy > 0.5 else 1 - base_accuracy

print("Base Accuracy {}".format(base_accuracy))

#           ######################################          #

#                   ##################                      #

#           ######################################          #


#   for three sides of the triangle
hidden_layer = keras.layers.Dense(units=3, activation=tf.keras.activations.sigmoid,
                                  bias_regularizer=tf.contrib.layers.l2_regularizer(0.00001),
                                  input_shape=(2,),
                                  use_bias=True,
                                  kernel_regularizer=tf.contrib.layers.l2_regularizer(0.00001),
                                  bias_initializer='TFRandomNormal',
                                  kernel_initializer='Orthogonal'
                                  )

#   for their sum
outer_layer = keras.layers.Dense(units=1, activation=tf.keras.activations.sigmoid,
                                 use_bias=True,
                                 bias_regularizer=tf.contrib.layers.l2_regularizer(0.00001),
                                 kernel_regularizer=tf.contrib.layers.l2_regularizer(0.00001),
                                 bias_initializer='TFRandomNormal',
                                 kernel_initializer='Orthogonal'
                                 )

triangle_learner = keras.models.Sequential()

triangle_learner.add(hidden_layer)
triangle_learner.add(outer_layer)

my_optimizer = keras.optimizers.Adam(lr=0.1)

my_loss_function = keras.losses.binary_crossentropy

triangle_learner.compile(optimizer=my_optimizer, loss=my_loss_function, metrics=['accuracy'])

training_data_x = tf.convert_to_tensor([(data[0], data[1]) for data in training_data])

training_data_y = tf.convert_to_tensor([data[2] for data in training_data])

triangle_learner.fit(training_data_x, training_data_y, epochs=5, steps_per_epoch=1000)

print(hidden_layer.get_weights())

print(outer_layer.get_weights())

testing_data_x = tf.convert_to_tensor([(data[0], data[1]) for data in testing_data])

testing_data_y = tf.convert_to_tensor([data[2] for data in testing_data])

predictions = triangle_learner.predict(x=testing_data_x, steps=10)


pyplot.plot([data[0] for data, prediction in zip(testing_data, predictions) if prediction[0] < 0.5],
            [data[1] for data, prediction in zip(testing_data, predictions) if prediction[0] < 0.5],
            'bo', c='0.8')

pyplot.plot([data[0] for data, prediction in zip(testing_data, predictions) if prediction[0] >= 0.5],
            [data[1] for data, prediction in zip(testing_data, predictions) if prediction[0] >= 0.5],
            'bo', c='0.2')

pyplot.xlim([min([data[0] for data in testing_data]), max([data[0] for data in testing_data])])
pyplot.ylim([min([data[1] for data in testing_data]), max([data[1] for data in testing_data])])

pyplot.grid()
pyplot.show()

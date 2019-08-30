import numpy as np
import tensorflow as tf
from tensorflow import keras

# This buggy behaviour was observed in tensorflow==1.14.0


my_x_array = np.array([1 for x in range(1000000)])
my_y_array = np.array([1 if x < 500000 else 0 for x in range(1000000)])

# We use two arrays, one input and output.
# We use x to be constant and y to hold 2 different values which are equally likely
# As we see, the minimum bayes error to predict 'y' from 'x' would be a minimum of 50%
#   (including the training error)

mirrored_strategy = tf.distribute.MirroredStrategy()
with mirrored_strategy.scope():
    hidden_layer = keras.layers.Dense(units=3, activation=tf.keras.activations.sigmoid,
                                      bias_regularizer=tf.contrib.layers.l2_regularizer(0.00001),
                                      input_shape=(1,),
                                      use_bias=True,
                                      kernel_regularizer=tf.contrib.layers.l2_regularizer(0.00001),
                                      bias_initializer='TFRandomNormal',
                                      kernel_initializer='Orthogonal'
                                      )

    #   for their sum
    outer_layer = keras.layers.Dense(units=1, activation=tf.keras.activations.sigmoid,
                                     use_bias=False,
                                     bias_regularizer=tf.contrib.layers.l2_regularizer(0.00001),
                                     kernel_regularizer=tf.contrib.layers.l1_regularizer(0.00001),
                                     bias_initializer='TFRandomNormal',
                                     kernel_initializer='Orthogonal'
                                     )

    triangle_learner = keras.models.Sequential()

    triangle_learner.add(hidden_layer)
    triangle_learner.add(outer_layer)

    my_optimizer = keras.optimizers.SGD(lr=0.1)

    my_loss_function = keras.losses.binary_crossentropy

    triangle_learner.compile(optimizer=my_optimizer, loss=my_loss_function, metrics=['accuracy'])
    print("Observe here that the accuracy begins with 100% which clearly must be a bug!")
    triangle_learner.fit(my_x_array, my_y_array, epochs=5, steps_per_epoch=500, batch_size=10, verbose=1)

np.random.shuffle(my_y_array)

with mirrored_strategy.scope():
    hidden_layer = keras.layers.Dense(units=3, activation=tf.keras.activations.sigmoid,
                                      bias_regularizer=tf.contrib.layers.l2_regularizer(0.00001),
                                      input_shape=(1,),
                                      use_bias=True,
                                      kernel_regularizer=tf.contrib.layers.l2_regularizer(0.00001),
                                      bias_initializer='TFRandomNormal',
                                      kernel_initializer='Orthogonal'
                                      )

    #   for their sum
    outer_layer = keras.layers.Dense(units=1, activation=tf.keras.activations.sigmoid,
                                     use_bias=False,
                                     bias_regularizer=tf.contrib.layers.l2_regularizer(0.00001),
                                     kernel_regularizer=tf.contrib.layers.l1_regularizer(0.00001),
                                     bias_initializer='TFRandomNormal',
                                     kernel_initializer='Orthogonal'
                                     )

    triangle_learner = keras.models.Sequential()

    triangle_learner.add(hidden_layer)
    triangle_learner.add(outer_layer)

    my_optimizer = keras.optimizers.SGD(lr=0.1)

    my_loss_function = keras.losses.binary_crossentropy

    triangle_learner.compile(optimizer=my_optimizer, loss=my_loss_function, metrics=['accuracy'])

    print("Shuffling the data explicitly resolves this")

    triangle_learner.fit(my_x_array, my_y_array, epochs=5, steps_per_epoch=500, batch_size=10, verbose=1)

my_x_array = np.array([1 for x in range(1000000)])
my_y_array = np.array([1 if x < 500000 else 0 for x in range(1000000)])

hidden_layer = keras.layers.Dense(units=3, activation=tf.keras.activations.sigmoid,
                                  bias_regularizer=tf.contrib.layers.l2_regularizer(0.00001),
                                  input_shape=(1,),
                                  use_bias=True,
                                  kernel_regularizer=tf.contrib.layers.l2_regularizer(0.00001),
                                  bias_initializer='TFRandomNormal',
                                  kernel_initializer='Orthogonal'
                                  )

#   for their sum
outer_layer = keras.layers.Dense(units=1, activation=tf.keras.activations.sigmoid,
                                 use_bias=False,
                                 bias_regularizer=tf.contrib.layers.l2_regularizer(0.00001),
                                 kernel_regularizer=tf.contrib.layers.l1_regularizer(0.00001),
                                 bias_initializer='TFRandomNormal',
                                 kernel_initializer='Orthogonal'
                                 )

triangle_learner = keras.models.Sequential()

triangle_learner.add(hidden_layer)
triangle_learner.add(outer_layer)

my_optimizer = keras.optimizers.SGD(lr=0.1)

my_loss_function = keras.losses.binary_crossentropy

triangle_learner.compile(optimizer=my_optimizer, loss=my_loss_function, metrics=['accuracy'])
print("Not observed when the distribute mirror strategy is not used.")
triangle_learner.fit(my_x_array, my_y_array, epochs=5, steps_per_epoch=500, batch_size=10, verbose=1)

np.random.shuffle(my_y_array)

hidden_layer = keras.layers.Dense(units=3, activation=tf.keras.activations.sigmoid,
                                  bias_regularizer=tf.contrib.layers.l2_regularizer(0.00001),
                                  input_shape=(1,),
                                  use_bias=True,
                                  kernel_regularizer=tf.contrib.layers.l2_regularizer(0.00001),
                                  bias_initializer='TFRandomNormal',
                                  kernel_initializer='Orthogonal'
                                  )

#   for their sum
outer_layer = keras.layers.Dense(units=1, activation=tf.keras.activations.sigmoid,
                                 use_bias=False,
                                 bias_regularizer=tf.contrib.layers.l2_regularizer(0.00001),
                                 kernel_regularizer=tf.contrib.layers.l1_regularizer(0.00001),
                                 bias_initializer='TFRandomNormal',
                                 kernel_initializer='Orthogonal'
                                 )

triangle_learner = keras.models.Sequential()

triangle_learner.add(hidden_layer)
triangle_learner.add(outer_layer)

my_optimizer = keras.optimizers.SGD(lr=0.1)

my_loss_function = keras.losses.binary_crossentropy

triangle_learner.compile(optimizer=my_optimizer, loss=my_loss_function, metrics=['accuracy'])

triangle_learner.fit(my_x_array, my_y_array, epochs=5, steps_per_epoch=500, batch_size=10, verbose=1)

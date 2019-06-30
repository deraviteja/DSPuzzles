from xor import xor_data_generator
import tensorflow as tf
from tensorflow import keras

xor_input, xor_output = xor_data_generator(size=1000)


hidden_layer = keras.layers.Dense(units=2, activation=tf.keras.activations.sigmoid,
                                  bias_regularizer=tf.contrib.layers.l2_regularizer(0.001),
                                  input_shape=(2,),
                                  use_bias=True,
                                  kernel_regularizer=tf.contrib.layers.l2_regularizer(0.001),
                                  bias_initializer='TFRandomNormal',
                                  kernel_initializer='Orthogonal'
                                  )

outer_layer = keras.layers.Dense(units=1, activation=tf.keras.activations.sigmoid,
                                 use_bias=True,
                                 bias_regularizer=tf.contrib.layers.l2_regularizer(0.0001),
                                 kernel_regularizer=tf.contrib.layers.l2_regularizer(0.0001),
                                 bias_initializer='TFRandomNormal',
                                 kernel_initializer='Orthogonal'
                                 )

xor_learner = keras.models.Sequential()

xor_learner.add(hidden_layer)
xor_learner.add(outer_layer)

my_optimizer = keras.optimizers.Adam(lr=0.1)

my_loss_function = keras.losses.binary_crossentropy

xor_learner.compile(optimizer=my_optimizer, loss=my_loss_function, metrics=['accuracy'])

training_data_x = tf.convert_to_tensor([(data[0], data[1]) for data in xor_input])

training_data_y = tf.convert_to_tensor([data for data in xor_output])


xor_learner.fit(training_data_x, training_data_y, epochs=5, steps_per_epoch=1000)

print(hidden_layer.get_weights())

print(outer_layer.get_weights())

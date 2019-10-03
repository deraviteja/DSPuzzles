import numpy as np
import tensorflow as tf
import datetime
import time
import sys

test_size = int(sys.argv[1])

cluster = tf.train.ClusterSpec({"master": ["localhost:2220"], "local": ["localhost:2222", "localhost:2223"]})
server = tf.train.Server(cluster, job_name="master", task_index=0)

flush_print = lambda key: print(key, flush=True)

# time.sleep(15)

with tf.device("/job:local/task:1"):
    # will run on localhost:2223
    first_batch = tf.Variable(initial_value=tf.random.normal([int(test_size/2), 1], dtype=tf.float32, mean=50))
    mean1 = tf.reduce_mean(first_batch)

with tf.device("/job:local/task:0"):
    # will run on localhost:2223
    second_batch = tf.Variable(initial_value=tf.random.normal([int(test_size/2), 1], dtype=tf.float32, mean=100))
    mean2 = tf.reduce_mean(second_batch)

with tf.device("/job:master/task:0"):
    # will run on localhost:2220
    mean = (mean1 + mean2) / 2

flush_print("Starting tensorflow session on master {}".format(datetime.datetime.now()))

with tf.Session("grpc://localhost:2220") as sess:
    sess.run(tf.global_variables_initializer())
    start_mean_calculation = datetime.datetime.now()
    flush_print("Initialized tensorflow variables {}, {}".format(start_mean_calculation, datetime.datetime.now()))
    result = sess.run(mean)
    end_of_mean_calculation = datetime.datetime.now()
    flush_print("Calculated the mean as {}, at {}, {} ".format(result, end_of_mean_calculation, datetime.datetime.now()))
    flush_print("Time takes in seconds {}".format((end_of_mean_calculation - start_mean_calculation).total_seconds()))


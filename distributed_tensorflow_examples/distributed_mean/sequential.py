import numpy as np
import sys
import datetime
import sys

size_of_array = int(sys.argv[1])

fflush_print = lambda key: print(key, flush=True)

start_time = datetime.datetime.now()
fflush_print("Starting sequential code at {start_time}. At {clock} ".format(start_time=start_time,
                                                                     clock=datetime.datetime.now()))

fflush_print("Starting to initialize random numpy array of size {}".format(size_of_array))

my_array = np.random.normal(loc=75, size=size_of_array)

start_mean_calculation = datetime.datetime.now()
fflush_print("Numpy array initialized at {}, Starting to calculate mean {}".format(start_mean_calculation,
                                                                            datetime.datetime.now()))
fflush_print("The mean is {}".format(np.mean(my_array)))
end_of_mean_calculation = datetime.datetime.now()
fflush_print("Numpy array mean calculated at {} , {}".format(end_of_mean_calculation,
                                                      datetime.datetime.now()))

fflush_print("Total time taken in seconds {}".format((end_of_mean_calculation - start_mean_calculation).total_seconds()))

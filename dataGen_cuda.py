# Try to save the model and resample it to see if it is faster

import time
import numba
import pandas as pd

from sdv import timeseries
from numba import jit
from numba import cuda

@jit()
def dataGen():

    loaded = timeseries.PAR.load('model_Conductividad.pkl')

    more_data = loaded.sample(1)

    print(more_data.head())
    print(len(more_data))

if __name__ == '__main__':

    # Get time with the GPU
    start = time.time()

    dataGen()
    cuda.profile_stop()

    end = time.time()

    print('Time elapsed in execution with GPU: ', end-start)

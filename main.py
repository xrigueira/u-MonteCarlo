
import numpy as np
import pandas as pd

from numba import jit
from numba import cuda
from datetime import datetime
from matplotlib import pyplot as plt

from dataGen import dataGen
from normalizer import normalizer
from filterer import filterer

"""Monte Carlo test to get the accuracy of the outlier detector proposed

How to generate synthetic data
https://sdv.dev/SDV/index.html
https://medium.com/geekculture/executing-a-python-script-on-gpu-using-cuda-and-numba-in-windows-10-1a1b10c29c9

"""

# Amonio, Conductividad, Nitratos, Oxigeno disuelto, pH, Temperatura, Turbidez
varName = 'Conductividad'
timeFrame = 'b'

if __name__ == '__main__':
    
    start = datetime.now()
    
    # Generate the data
    dataGen(varName=varName)
    
    # No need to check gaps because we are starting from the _full.csv which is the result of checkGaps.py
    
    # Normalize the data. See normalizer.py for details
    normalizer(File=f'{varName}_gen.csv')
    print('[INFO] normalizer() DONE -> Preprocessing completed')
    
    # Filter out those time units with too many NaN and iterate on the rest
    # The only gaps will be the inserted days in normalizer so this function has to be calleds despite that
    # there are no other nans
    filterer(File=f'{varName}_nor.csv', timeframe=timeFrame)
    print('[INFO] filterer() DONE -> Preprocessing completed')
    
    end = datetime.now()

    print("Time elapsed in execution:", end-start)
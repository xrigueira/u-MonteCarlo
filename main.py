
from sys import _xoptions
import numpy as np
import skfda as fda
import pandas as pd

from numba import jit
from numba import cuda
from datetime import datetime
from matplotlib import pyplot as plt

from checkGaps import checkGaps
from dataGen import dataGen
from normalizer import normalizer
from filterer import filterer
from builder import builder
from uFda import functionalAnalysis

"""Monte Carlo test to get the accuracy of the outlier detector proposed

How to generate synthetic data
https://sdv.dev/SDV/index.html
https://medium.com/geekculture/executing-a-python-script-on-gpu-using-cuda-and-numba-in-windows-10-1a1b10c29c9

"""
def x_selector(varName):

    if varName == 'Caudal':
        x = 1.1
    elif varName == 'Conductividad':
        # x = 0.72 for full
        x = 1.1
    elif varName == 'Nitratos':
        x = 1.45
    elif varName == 'Oxigeno disuelto':
        x = 1.34
    elif varName == 'pH':
        x = 1.4
    elif varName == 'Temperatura':
        x = 1.81

    return x

# Amonio, Caudal, Conductividad, Nitratos, Oxigeno disuelto, pH, Temperatura, Turbidez
varName = 'Conductividad'
timeFrame = 'b'

if __name__ == '__main__':
    
    start = datetime.now()

    # Generate the data (optional)
    # x = x_selector(varName=varName)
    # dataGen(File=f'{varName}.txt', x=x)
    # print('[INFO] dataGen() DONE')

    # Fill in the gaps in the time series
    # checkGaps(File=f'{varName}_gen.csv')
    checkGaps(File=f'{varName}.txt')
    print('[INFO] checkGaps() DONE')

    # Normalize the data. See normalizer.py for details
    normalizer(File=f'{varName}_full.csv')
    print('[INFO] normalizer() DONE')
    
    # Filter out those time units with too many NaN and iterate on the rest
    # The only gaps will be the inserted days in normalizer so this function has to be called despite that
    # there are no other nans
    filterer(File=f'{varName}_nor.csv', timeframe=timeFrame)
    print('[INFO] filterer() DONE')

    # Read the database with the desired time unit and create dataMatrix and timeStamps
    dataMatrix, timeStamps = builder(File=f'{varName}_pro.csv', timeFrame=timeFrame)
    print('[INFO] builder() DONE')

    cutoffIntBox, cutoffMDBBox, cutoffIntMS, cutoffMDBMS = 1, 1, 0.993, 0.993 # Cutoff params

    # Define depths here
    integratedDepth = fda.exploratory.depth.IntegratedDepth().multivariate_depth
    modifiedbandDepth = fda.exploratory.depth.ModifiedBandDepth().multivariate_depth
    projectionDepth = fda.exploratory.depth.multivariate.ProjectionDepth()
    simplicialDepth = fda.exploratory.depth.multivariate.SimplicialDepth()
    
    outliers, outliersBoosted = functionalAnalysis(varname=varName, depthname='modified band', datamatrix=dataMatrix, timestamps=timeStamps, timeframe=timeFrame, depth=modifiedbandDepth, cutoff=cutoffIntMS)
    print('[INFO] functionalAnalysis() DONE')
    
    # The MC loop has to start here
        
    end = datetime.now()

    print("Time elapsed in execution:", end-start)
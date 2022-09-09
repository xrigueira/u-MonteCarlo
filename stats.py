import numpy as np
import pandas as pd
from scipy import stats

from matplotlib import pyplot as plt

"""This does a basic statistical analysis of the data
including max, min, mean, median, mode, quartiles, normality
test etc.
"""

def statsAnalysis(varName):
    Maxim = max(df[varName]) # Max value of the variable
    Minim = min(df[varName]) # Min value of the variable
    Mean = np.mean(df[varName]) # Mean of the data studied
    Mode = stats.mode(df[varName]) # Mode of the data studied
    Std = np.std(df[varName]) # Standard deviation of the data
    Variance = np.var(df[varName]) # Variance of the data

    Q1 = np.percentile(df[varName], 25) # Primer quartile
    Q2 = np.percentile(df[varName], 50) # Segundo quartile
    Q3 = np.percentile(df[varName], 75) # Tercer quartile
    InQR = Q3 - Q1 # Inter quartile range
    
    return Maxim, Minim, Mean, Mode, Std, Variance, Q1, Q2, Q3, InQR

def normalDistribution(varName):
    varList = df[varName].to_list()

    # dataNormal = np.random.normal(Mean, Std, len(varList))

    # count, bins, ignored = plt.hist(dataNormal, bins=numberBins(varName), alpha = 0.5, label='normal distribution')
    count, bins, ignored = plt.hist(df[varName], bins=numberBins(varName), alpha = 0.5, label=f'{varName}') # Histogram
    plt.legend()
    plt.show()

    statistics, p = stats.normaltest(df[varName]) # Preguntar si esto no debería dar que es una distribución normal (a Javi en la reunión).
    print('h value: {} | p value: {}'.format(statistics, p))

    if p < 0.05: # null hypothesis: the data comes froma normal distribution
        print('The null hypothesis can be rejected')
    elif p  > 0.05:
        print('The null hypothesis cannot be rejected')

    """Se rechaza la hipótesis nula (h=1) si el nivel de significancia es del 5%, esto es, si el valor de p 
    es menor que 0.05. Si el valor de p es mayor que 0.05, h será 0)."""
    
    return varList, count, bins

def numberBins(varName):
    data = df[varName].to_list()
    n = len(data) # number of observations
    range = max(data) - min(data) 
    numIntervals = np.sqrt(n) 
    width = range/numIntervals # width of the intervals
    
    return np.arange(min(data), max(data), width).tolist()

def boxplot(varName, Q1, Q3, InQR):
    plt.boxplot(df[varName])
    
    upperBound = Q3 + (1.5*InQR)
    lowerBound = Q1 - (1.5*InQR)
    
    outliersBoxplot = df[(df[varName] <= lowerBound) | (df[varName] >= upperBound)]
    # pd.set_option("display.max_rows", None, "display.max_columns", None)
    print('These are the outliers in the boxplot:', outliersBoxplot)
    print(len(outliersBoxplot))
    plt.show()
    
    return outliersBoxplot

varName = 'Valor'
fileName = 'Turbidez'
df = pd.read_csv(f'Database/{fileName}.txt', delimiter=';', parse_dates=['Fecha'])

if __name__ == '__main__':

    # Statistical analysis
    Maxim, Minim, Mean, Mode, Std, Variance, Q1, Q2, Q3, InQR = statsAnalysis(varName) 
    print('Maximum: {}; Minimum: {}; Mean: {}; Q1: {}; Q3: {}; IQR: {}'. format(Maxim, Minim, Mean, Q1, Q3, InQR))

    # Test de distribución normal
    varList, count, bins = normalDistribution(varName)

    # Boxplot
    # outliersBoxplot = boxplot(varName, Q1, Q3, InQR)
    
    # plt.show()
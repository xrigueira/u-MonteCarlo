import numpy as np
import pandas as pd

"""This file implements the detection of those value
above the legal limits of pollution in water bodies."""

File = 'data_pro.csv'
df = pd.read_csv(f'Database/{File}', delimiter=';', parse_dates=['date'], index_col=['date'])

# Get those rows above the limit
result = df.loc[df['ammonium'] >= 0.2]

# In the case a multivariate condition
result = df.loc[(df['ammonium'] >= 0.2) & (df['conductivity'] > 875)]

print(result)

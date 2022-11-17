# See how to get the index to use it in the shape contamination model

import math
import numpy as np
import pandas as pd

df = pd.read_csv('Database/Conductividad_pro.csv', delimiter=';')

# new_outliers = [9, 18, 32]
new_outliers = [6, 9, 18, 32]
print((df.loc[df['week'] == 9]))
# Generate the shape outliers
for i in new_outliers:

    # Extract the maximum and minimum of the database
    maximum, mean, minimum = max(df.loc[:, 'value']), np.mean(df.loc[:, 'value']), min(df.loc[:, 'value'])
    p90, p10 = np.percentile(df.loc[:, 'value'], 90), np.percentile(df.loc[:, 'value'], 10)
    print(maximum, minimum)
    # print(p90, p10)

    target = np.mean(df.loc[df['week'] == i, 'value'])
    print('target', target)

    # Get the distances to max and min
    dist2max, dist2min = maximum - target, target - minimum

    # Now define mag_factor based on whether the target is close to the max or min
    if dist2min < dist2max:

        print('por debajo')

        mag_factor = ((minimum / target) - (1 - (target / mean)))
    
    elif dist2min > dist2max:

        print('por arriba')

        mag_factor = ((maximum / target) - (1 - (mean / target)))
    
    print(mag_factor)

# See how to get the index to use it in the shape contamination model

import math
import pandas as pd

df = pd.read_csv('Database/Conductividad_con.csv', delimiter=';')

# new_outliers = [9, 18, 32]
new_outliers = [9]
print((df.loc[df['week'] == 9]))
# Generate the shape outliers
for i in new_outliers:

    df_subset = df.loc[df['week'] == i]

    indices = list(df_subset.index)
    for j in indices:

        # df_subset.value = df_subset.apply(lambda row: (row.value * (1 + (0.01 * math.sin(0.5 * j)))) if row.name == j else row.value, axis=1)
        # df_subset.outlier = df_subset.apply(lambda row: 1 if row.name == j else row.outlier, axis=1)
        
        # Testing new method
        df.loc[j, 'value'] = df.loc[j, 'value'] * (1 + (0.01 * math.sin(0.5 * j)))
        df.loc[j, 'outlier'] = 1
        # print((df.loc[df['week'] == 9]).head(10))

    
    # new_outliers.remove(i)
    # input_outliers.append(i)

# df.loc[indices[0]:indices[-1], 'value'] = df_subset['value']

print((df.loc[df['week'] == 9]))



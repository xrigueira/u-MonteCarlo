import math
import random
import numpy as np
import pandas as pd

def mag_factor_calc(dataframe, i):

    # Extract the maximum and minimum of the database
    maximum, mean, minimum = max(dataframe.loc[:, 'value']), np.mean(dataframe.loc[:, 'value']), min(dataframe.loc[:, 'value'])
    # p90, p10 = np.percentile(dataframe.loc[:, 'value'], 90), np.percentile(dataframe.loc[:, 'value'], 10)

    # Get the mean of the target time interval (month, week, day)
    target = np.mean(dataframe.loc[dataframe['week'] == i, 'value'])

    # Get the distances to max and min
    dist2max, dist2min = maximum - target, target - minimum

    # Now define mag_factor based on whether the target is close to the max or min
    if dist2min < dist2max: # lower half

        mag_factor = ((minimum / target) - (1 - (target / mean)))
    
    elif dist2min > dist2max: # upper half

        mag_factor = ((maximum / target) + (1 - (mean / target)))
    
    
    return(mag_factor)


def magnitude_outliers(df_clean, new_outliers, num_cont_outliers, input_outliers):
    
    # Generate the magnitude outliers
    for i in new_outliers[0:num_cont_outliers]:

        # mag_factor = random.choice([random.uniform(-1.5, -0.75), random.uniform(2.5, 4.5)])
        mag_factor = mag_factor_calc(dataframe=df_clean, i=i)
        df_clean.value = df_clean.apply(lambda row: (row.value * mag_factor) if row.week == i else row.value, axis=1)
        df_clean.outlier = df_clean.apply(lambda row: 1 if row.week == i else row.outlier, axis=1)

        new_outliers.remove(i)
        input_outliers.append(i)
    
    return(df_clean, new_outliers, input_outliers)

def shape_outliers(df_clean, new_outliers, num_cont_outliers, input_outliers):

    # Generate the shape outliers
    for i in new_outliers[0:num_cont_outliers]:
        
        df_subset = df_clean.loc[df_clean['week'] == i]
        
        indices = list(df_subset.index)
        for j in indices:
            
            df_clean.loc[j, 'value'] = df_clean.loc[j, 'value'] * (1 + (0.2 * math.sin(0.05 * j)))
            df_clean.loc[j, 'outlier'] = 1
        
        new_outliers.remove(i)
        input_outliers.append(i)
    
    # Old method
    # for i in new_outliers[0:num_cont_outliers]:

    #     df_clean.value = df_clean.apply(lambda row: (row.value + row.value * (0.025 * math.sin(100000 * row.value))) if row.week == i else row.value, axis=1)
    #     df_clean.outlier = df_clean.apply(lambda row: 1 if row.week == i else row.outlier, axis=1)

    #     new_outliers.remove(i)
    #     input_outliers.append(i)
    
    return(df_clean, new_outliers, input_outliers)

def mixed_outliers(df_clean, new_outliers, num_cont_outliers, input_outliers):

    # Generate the mixed outliers
    for i in new_outliers[0:num_cont_outliers]:
        
        # mag_factor = random.choice([random.uniform(-1.5, -0.75), random.uniform(2.5, 4.5)])
        mag_factor = mag_factor_calc(dataframe=df_clean, i=i)
        
        df_subset = df_clean.loc[df_clean['week'] == i]
        
        indices = list(df_subset.index)
        
        for j in indices:
            
            df_clean.loc[j, 'value'] = (df_clean.loc[j, 'value'] * (1 + (0.2 * math.sin(0.05 * j)))) * mag_factor
            df_clean.loc[j, 'outlier'] = 1
        
        new_outliers.remove(i)
        input_outliers.append(i)
    
    # Old method
    # for i in new_outliers[0:num_cont_outliers]:

    #     mag_factor = random.choice([random.uniform(-1.5, -0.75), random.uniform(1.5, 2.5)])
    #     df_clean.value = df_clean.apply(lambda row: ((row.value + row.value * (0.025 * math.sin(100000 * row.value))) * mag_factor) if row.week == i else row.value, axis=1)
    #     df_clean.outlier = df_clean.apply(lambda row: 1 if row.week == i else row.outlier, axis=1)

    #     new_outliers.remove(i)
    #     input_outliers.append(i)
    
    return(df_clean, new_outliers, input_outliers)

def outlier_generator(varname, timeframe, outliersBoosted):

    # Delete the outliers depending on the timeFrame chosen
    if timeframe == 'a':
        
        # This should operate in a similar way to timeFrame == 'c'
        print('This timeFrame option has not been implemented yet.')
        pass  
    
    elif timeframe == 'b': 
        
        # Read the data base processed
        df = pd.read_csv(f'Database/{varname}_pro.csv', delimiter=';')
        
        # Split the start and end dates
        outliers_clean = [i.split(',') for i in outliersBoosted]
        outliers_startDate = [i[0][2:-1] for i in outliers_clean]
        outliers_endDate = [i[1][2:-2] for i in outliers_clean]

        # Get the week nunmber of the outlying weeks
        outlying_weeks = []
        for i in outliers_startDate:
            
            index = df.loc[df['startDate'] == i, 'week'].iloc[0]
            outlying_weeks.append(index)
        
        print('Original outliers:', outlying_weeks)
        
        # Delete those rows with week in outling_weeks
        for i in outlying_weeks:

            df = df.drop(df[df['week'] == int(i)].index, inplace=False)
        
        # Assign the cleaned dataframe to a new variable
        df_clean = df.copy()

    elif timeframe == 'c':
        
        print('This timeFrame option has not been implemented yet.')
        pass
        
        # Here is left what I had developed for timeFrame 'c'
        outliersBoosted = ['2 1 2019', '22 1 2019', '23 1 2019', '29 1 2019', '30 1 2019', '31 1 2019', '12 2 2019', '5 4 2019', '26 4 2019', '22 5 2019', '6 7 2019', '14 11 2019', '15 11 2019', '16 11 2019', '17 11 2019', '18 11 2019', '26 11 2019', '16 12 2019', '17 12 2019', '18 12 2019', '19 12 2019', '20 12 2019', '24 12 2019', '25 12 2019', '26 12 2019', '27 12 2019', '13 3 2020', '14 3 2020', '15 3 2020', '20 3 2020', '21 3 2020', '22 3 2020', '3 4 2020', '3 5 2020', '31 5 2020', '3 6 2020', '3 7 2020', '3 8 2020', '10 8 2020', '3 9 2020', '3 10 2020', '15 10 2020', '3 11 2020', '3 12 2020', '14 12 2020', '15 12 2020', '16 12 2020', '17 12 2020', '2 1 2021', '10 1 2021', '11 1 2021', '16 1 2021', '19 1 2021', '23 1 2021', '24 1 2021', '25 1 2021', '28 1 2021', '29 1 2021', '30 1 2021', '31 1 2021', '10 2 2021', '11 2 2021', '14 2 2021', '2 3 2021', '11 3 2021', '12 3 2021', '21 3 2021', '29 3 2021', '2 4 2021', '11 4 2021', '12 4 2021', '2 5 2021', '9 5 2021', '10 5 2021', '11 5 2021', '12 5 2021', '10 6 2021', '11 6 2021', '12 6 2021', '13 6 2021', '6 7 2021', '9 7 2021', '10 7 2021', '11 7 2021', '2 8 2021', '9 8 2021', '10 8 2021', '11 8 2021', '12 8 2021', '2 9 2021', '9 9 2021', '10 9 2021', '11 9 2021', '12 9 2021', '13 9 2021', '15 9 2021', '16 9 2021', '18 9 2021', '19 9 2021', '20 9 2021', '21 9 2021', '22 9 2021', '23 9 2021', '24 9 2021', '26 9 2021', '30 9 2021', '9 10 2021', '10 10 2021', '11 10 2021', '12 10 2021', '13 10 2021', '16 10 2021', '17 10 2021', '18 10 2021', '19 10 2021', '20 10 2021', '21 10 2021', '22 10 2021', '23 10 2021', '24 10 2021', '25 10 2021', '26 10 2021', '27 10 2021', '28 10 2021', '29 10 2021', '30 10 2021', '31 10 2021', '2 11 2021', '9 11 2021', '10 11 2021', '11 11 2021', '14 11 2021', '19 11 2021', '9 12 2021', '10 12 2021', '13 12 2021', '14 12 2021']

        outliers_clean = [i.split(' ') for i in outliersBoosted]

        # Based on this information contained in outliers_clean I have to get the index where it starts and ends each outlying day
        day = [i[0] for i in outliers_clean]
        month = [i[1] for i in outliers_clean]
        year = [i[2] for i in outliers_clean]

        indexInit = []
        indexEnd = []
        for i, j, k in zip(day, month, year):
            
            indices = (df.loc[(df['day'] == int(i)) & (df['month'] == int(j)) & (df['year'] == int(k))]).index

            indexInit.append(indices[0])
            indexEnd.append(indices[-1])

        counter = 0
        lenDay = 96
        for i in zip(indexInit, indexEnd):
            
            df = df.drop(df.index[int(i-counter*lenDay):int(j-counter*lenDay+1)], inplace=False)
            counter += 1

    # Mark all rows as no outliers with a new column of zeros
    df_clean['outlier'] = 0

    # Contaminate the database
    # Get a 15% of random weeks to define the number of outliers
    weeks = list(dict.fromkeys(df_clean['week'].tolist()))
    weeks = [i for i in weeks if i != 0]

    num_outliers = int(len(weeks) * 0.15)

    # Draw num_outliers randomly from weeks
    new_outliers = random.sample(weeks, num_outliers)

    # Define how many weeks will be outliers in each model (33 % of num_outliers)
    num_cont_outliers = int(len(new_outliers) / 3)

    input_outliers = [] # This is needed because num_outliers my not be divisible by 3
    
    # Call the functions for the contamination models
    df_clean, new_outliers, input_outliers = magnitude_outliers(df_clean, new_outliers, num_cont_outliers, input_outliers)

    df_clean, new_outliers, input_outliers = shape_outliers(df_clean, new_outliers, num_cont_outliers, input_outliers)

    df_clean, new_outliers, input_outliers = mixed_outliers(df_clean, new_outliers, num_cont_outliers, input_outliers)

    # Save df_clean
    cols = list(df_clean.columns.values.tolist())
    df_clean.to_csv(f'Database/{varname}_con.csv', sep=';', encoding='utf-8', index=False, header=cols)
    
    return(input_outliers)




import pandas as pd

timeFrame = 'b'
outliersBoosted = ["('2019 12 2', '2019 12 8')", "('2020 3 7', '2020 3 13')", "('2020 9 24', '2020 9 30')", "('2020 12 15', '2020 12 21')", "('2020 12 29', '2021 1 4')", "('2021 1 12', '2021 1 18')", "('2021 1 19', '2021 1 25')", "('2021 2 2', '2021 2 8')", "('2021 2 9', '2021 2 15')", "('2021 5 21', '2021 5 27')", "('2021 10 6', '2021 10 12')", "('2021 10 13', '2021 10 19')", "('2021 10 20', '2021 10 26')", "('2021 10 27', '2021 11 2')", "('2021 11 3', '2021 11 9')", "('2021 12 14', '2021 12 20')"]

def deleter(timeframe, outliersBoosted):

    if timeFrame == 'a':
        
        # This should operate in a similar way to timeFrame == 'c'
        print('This timeFrame option has not been implemented yet.')
        pass
        
    
    elif timeframe == 'b': 
        
        # Read the data base processed
        df = pd.read_csv(f'Database/Conductividad_pro.csv', delimiter=';')
        
        # Split the start and end dates
        outliers_clean = [i.split(',') for i in outliersBoosted]
        outliers_startDate = [i[0][2:-1] for i in outliers_clean]
        outliers_endDate = [i[1][2:-2] for i in outliers_clean]

        # Get the week nunmber of the outlying weeks
        outlying_weeks = []
        for i in outliers_startDate:
            
            index = df.loc[df['startDate'] == i, 'week'].iloc[0]
            outlying_weeks.append(index)
        
        # Delete those rows with week in outling_weeks
        for i in outlying_weeks:
            
            df = df.drop(df[df['week'] == i].index, inplace=False)


    elif timeFrame == 'c':
        
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

    return(df)

df = deleter(timeframe=timeFrame, outliersBoosted=outliersBoosted)

# Contuar metiendo los modelos de contaminación


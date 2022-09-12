import os
import numpy as np
import pandas as pd

from numba import jit
from numba import cuda
from datetime import datetime
from matplotlib import pyplot as plt
from pearson import pearson_correlation

# Results of the ideal "x" values for each variable
# x = [1, 1.1 0.72, 1.45, 1.34, 1.4, 1.81] # Amonio, Caudal Conductividad, Nitratos, Oxigeno disuelto, pH, Temperatura, Turbidez

def dataGen(File, x):

    # Load the original data
    fileName, fileExtension = os.path.splitext(File)
    df = pd.read_csv(f'Database/{fileName}.csv', delimiter=';', parse_dates=['date'])
    # df['value'].plot(alpha=0.5)

    # Clean data to get the variation 
    data = df['value'].to_list()
    data_clean = [i for i in data if np.isnan(i) == False]

    # Get the average amount of variation
    quotient = []
    for i, e in enumerate(data_clean):

        if i == len(data_clean):
            break

        if data_clean[i-1] != 0:
            result = abs(data_clean[i]-data_clean[i-1])/data_clean[i-1] # Calculates the variation between consec. data points
            quotient.append(result)

    variation = np.average(quotient)

    # Get the index when there is a change from a NaN to a no-NaN
    nan_jumps = []
    for i, e in enumerate(data):
        
        if np.isnan(data[i-1]) == True and np.isnan(data[i]) == False:

            nan_jumps.append(i)

    # Generate data 
    date_rng = pd.date_range(start=str(df['date'].tolist()[0]), end=str(df['date'].tolist()[-1]), freq='15min')
    df_gen = pd.DataFrame(date_rng, columns=['date'])

    counter = 0
    nan_situation = False
    generated_data = []
    for i, e in enumerate(data):

        # Condition at the start of the loop
        if i == 0:
            firts_point = data[0]
        
            data_point = np.random.uniform((firts_point*(1-abs(variation))), (firts_point*(1+variation)), size=1)
        
            generated_data.append(data_point)
        
        else:

            # Calculate the local variation
            if nan_situation == False:

                local_variation = ((data[i]-data[i-1])/(data[i-1]))/1

                if np.isnan(local_variation) == True:

                    local_variation = ((data[nan_jumps[counter]]-data[i-1])/(data[i-1]))/(nan_jumps[counter]-i)
                    local_variation = local_variation/x # O2 1.3

                    counter += 1

                    nan_situation = True
            
            elif nan_situation == True:

                if i == nan_jumps[counter-1]:
                    nan_situation = False
                
                local_variation = local_variation

            preceeding_point = generated_data[-1]

            # Generate the new data points based on the preceeding point and the local variation
            if local_variation < 0:
                
                data_point = np.random.uniform((preceeding_point*(1-abs(local_variation))), preceeding_point, size = 1)

                generated_data.append(data_point)

            elif local_variation == 0:

                data_point = preceeding_point

                generated_data.append(data_point)
            
            elif local_variation > 0:
                    
                data_point = np.random.uniform(preceeding_point, (preceeding_point*(1+local_variation)), size=1)

                generated_data.append(data_point)


    df_gen['value'] = np.array(generated_data)
    # df_gen['value'].plot(alpha=0.5)

    # plt.show()

    # Save the database generated as csv
    df.to_csv(f'Database/{varName}_gen.csv', sep=';', encoding='utf-8', index=False, header=['date', 'value'])

    return data, data_clean, generated_data


if __name__ == '__main__':

    start = datetime.now()
    # Amonio, Caudal, Conductividad, Nitratos, Oxigeno disuelto, pH, Temperatura, Turbidez
    varName = 'Caudal'
    
    # dataGen(File=f'{varName}_full.csv', x = x)

    # The rest of the code is to calculate the optimum value of "x"
    x_list = []
    rho_list = []
    for x in np.arange(0.01, 2, 0.01):

        x = round(x, 3)
        
        data, data_clean, generated_data = dataGen(File=f'{varName}_full.csv', x = x)

        # Delete those points in generated_data for which data has nan.
        generated_data_clean = []
        for i, j in zip(data, generated_data):

            if np.isnan(i) == False:

                generated_data_clean.append(j)
        
        rho = pearson_correlation(data_clean, generated_data_clean)

        x_list.append(x)
        rho_list.append(rho)
    
    plt.plot(rho_list)
    plt.xticks(np.arange(len(x_list)), x_list)
    plt.show()

    print('Ideal x:', x_list[rho_list.index(max(rho_list))])

    end = datetime.now()

    print('Time elapsed: {}'.format(end - start))

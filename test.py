import numpy as np

from matplotlib import pyplot as plt

data = [171, 173, 174, np.nan, np.nan, 170, 176, 180, np.nan, np.nan, np.nan, 190, 173]

data_clean = [i for i in data if np.isnan(i) == False]
maximum = np.max(data_clean)
minimum = np.min(data_clean)

# Get the average amount of variation
quotient = []
for i, e in enumerate(data_clean):

    if i == len(data_clean):
        break

    if data_clean[i-1] != 0:
        result = abs(data_clean[i]-data_clean[i-1])/data_clean[i-1] # Calculates the variation between consec. data points
        quotient.append(result)

variation = np.average(quotient)
print(variation)

# Get the index when there is a change from a NaN to a no-NaN
nan_jumps = []
for i, e in enumerate(data):
    
    if np.isnan(data[i-1]) == True and np.isnan(data[i]) == False:

        nan_jumps.append(i)

counter = 0
nan_situation = False
generated_data = []
for i, e in enumerate(data):

    # Condition at the start of the loop
    if i == 0:
        firts_point = data[0]
    
        data_point = np.random.uniform((firts_point*(1-variation)), (firts_point*(1+variation)), size=1)
    
        generated_data.append(data_point)
    
    else:

        # Calculate the local variation
        if nan_situation == False:

            local_variation = (data[i]-data[i-1])/(data[i-1])

            if np.isnan(local_variation) == True:

                # local_variation = (data[nan_jumps[counter]]-data[i-1])/data[i-1]
                local_variation = (data[nan_jumps[counter]]-data[i-1])/(data[i-1])
                local_variation = local_variation/(nan_jumps[counter]-i)

                counter += 1

                nan_situation = True
        
        elif nan_situation == True:

            if i == nan_jumps[counter-1]:
                nan_situation = False
            
            local_variation = local_variation

        preceeding_point = generated_data[-1]

        if local_variation < 0:
            
            if nan_situation == True:
                data_point = np.random.uniform((preceeding_point*(1-abs(local_variation))), preceeding_point, size = 1)
            
            else:
                data_point = np.random.uniform((preceeding_point*(1-abs(variation))), preceeding_point, size = 1)

            generated_data.append(data_point)

        elif local_variation == 0:

            data_point = preceeding_point

            generated_data.append(data_point)
        
        elif local_variation > 0:
            
            if nan_situation == True:
                
                data_point = np.random.uniform(preceeding_point, (preceeding_point*(1+local_variation)), size=1)

            else:

                data_point = np.random.uniform(preceeding_point, (preceeding_point*(1+variation)), size=1)

            generated_data.append(data_point)

        print(local_variation)

plt.plot(data)
plt.plot(generated_data)

plt.show()
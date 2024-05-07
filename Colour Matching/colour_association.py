# The input to this code is from segmentation of the map image and from the OCR data extraction.
# The segmentation input file containsthe type of map image(discrete or colour bar) followed by the states and their average colour value in RGB format.
# The OCR input file contains the Title of the map image along with the data present in the image - the values along with their
# corresponding colour value in RGB format.

import numpy as np
import pandas as pd

df = pd.read_csv('Result.csv')
df =  df[['State_Name']]
# print(df)

def getDataForFilename(output_data, filename):
    return [tuple for tuple in output_data if tuple[0] == filename]

def getUniqueFilenames(ocr_df):
    return ocr_df['file_name'].unique().tolist()

def getMapTitleDictionary(ocr_df, filenames_list):
    map_dict = {}
    for filename in filenames_list:
        filtered_rows = ocr_df[ocr_df['file_name'] == filename]
        row = filtered_rows.iloc[0]
        # print(row)
        map_dict[filename] = row['map_title']
    
    return map_dict

ocr_df = pd.read_csv("Input_Files/OCR_set1.csv")
seg_df = pd.read_csv("Input_Files/Segmentation_set1.csv")
data_a = []
data_b = []

rows, cols = seg_df.shape
# iterating through each row and selecting
# 'File Name', 'State' and 'RGB Colour' column respectively.
for row in seg_df.itertuples():
    file_name = row[1]
    state = row[2]
    color = row[6]
    color = tuple(int(x) for x in color.strip('()').split(','))
    data_a.append((file_name, state, color))

rows, cols = ocr_df.shape
# iterating through each row and selecting
# 'File Name', 'Map Type', 'Map Title', 'RGB Colour', 'Value' and 'Unit' column respectively.
for row in ocr_df.itertuples():
    file_name = row[1]
    map_type = row[2]
    map_title = row[3]
    color = row[4]
    color = tuple(int(x) for x in color.strip('()').split(','))
    value = row[5]
    if value != "'N/A'":
        average_value = float(value)
    else:
        average_value = 0
    unit = row[6]
    data_b.append((file_name, map_type, map_title, color, average_value, unit))

# Performing colour association/matching to assign values to each state present in the map image, hence preparing data for analysis.
# The logic used for the 2 different types of map images is different, hence using the data stored in variable map_type, we have separated out the 2 algorithms.

# In images containing Discrete Legends, the colour associated with the states must be one of the values associated to the legends, hence a simple
# Euclidean distance evaluation metric is suitable to calculate the value corresponding to each state.

# In images containing Colour Bar, the colour associated with the states could lie anywhere in the colour bar and hence, we leverage the piecewise linear
# interpolation method to obtain the value corresponding to each state.

output_data = []

for file_name, state, state_color in data_a:

    numerical_data = []

    for file, map_type, map_title, color, average_value, unit in data_b:
        if file_name == file:
            mapType = map_type
            numerical_data.append((map_title, map_type, color, average_value, unit))
    if mapType == "discrete":
        min_distance = float('inf')
        # print(numerical_data)
        assigned_value = None
        assigned_unit = None
        for map_title, map_type, color, average_value, unit in numerical_data:
            # calculating Euclidean distance
            distance = sum((c1 - c2) ** 2 for c1, c2 in zip(state_color, color))
            if distance < min_distance:
                min_distance = distance
                assigned_value = average_value
                assigned_unit = unit
        output_data.append((file_name, state, assigned_value, assigned_unit))
    elif mapType == "continuous":
        assigned_value = 0
        # print(numerical_data)
        assigned_unit = numerical_data[0][4]
        for i in range(len(numerical_data) - 1):
            delta=0
            flag_1=0
            flag_2=0
            if i==0:
                delta=0.5
                flag_1=1
            elif i==len(numerical_data)-2:
                delta=-0.5
                flag_2=1
                
            # Extract legend numbers, colors, and average values for the current and next entry
            colour_1, value_1 = numerical_data[i][2], numerical_data[i][3]
            colour_2, value_2 = numerical_data[i + 1][2], numerical_data[i + 1][3]
            # print(value_1)
            # print(value_2)

            # Calculate alpha using the formula
            A = []

            for i in range(0,3):
                if colour_1[i] != colour_2[i]:
                    A.append((state_color[i] - colour_2[i]) / (colour_1[i] - colour_2[i]))
        
            if A:
                A = sum(A) / len(A)
            else:
                A = 0
            
            if (0+flag_2*delta)<=A and A<=(1+flag_1*delta):
                assigned_value = A*(value_1-value_2)+value_2
        output_data.append((file_name, state, assigned_value, assigned_unit))

file_list = getUniqueFilenames(ocr_df)
map_titles = getMapTitleDictionary(ocr_df, file_list)

for filename in file_list:
    dataReqd = getDataForFilename(output_data, filename)
    map_title = map_titles[filename]
    df[map_title] = 0

    for filename, state, assigned_value, assigned_unit in dataReqd:
        value = str(assigned_value)+assigned_unit
        # print(value)
        df.loc[df['State_Name'] == state, map_title] = value

# print(df['Health Insurance Coverage of Men 19-24 | KFF'])
df.to_csv('Result.csv',index = False)
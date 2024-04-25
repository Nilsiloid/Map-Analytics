# The input to this code is from segmentation of the map image and from the OCR data extraction.
# The segmentation input file containsthe type of map image(discrete or colour bar) followed by the states and their average colour value in RGB format.
# The OCR input file contains the Title of the map image along with the data present in the image - the values along with their
# corresponding colour value in RGB format.

import numpy as np
import pandas as pd

df = pd.read_csv('Result.csv')
ocr_df = pd.read_csv("OCR_output.csv")
seg_df = pd.read_csv("Segmentation_output.csv")

output_data = []
data_a = []
data_b = []

map_type = ""
map_title = ""
map_name = ""


rows, cols = seg_df.shape
# iterating through each row and selecting
# 'Class Name' and 'RGB Colour' column respectively.
for row in seg_df.itertuples():
    file_name = row[1]
    state = row[2]
    color = row[6]
    data_a.append((file_name, state, color))

rows, cols = ocr_df.shape
for row in ocr_df.itertuples():
    file_name = row[1]
    map_type = row[2]
    map_title = row[3]
    color = row[4]
    value = row[5]
    if value != "'N/A'":
        average_value = float(value)
    else:
        average_value = 0
    unit = row[6]
    data_b.append(file_name, map_type, map_title, color, average_value, unit)

# Performing colour association/matching to assign values to each state present in the map image, hence preparing data for analysis.
# The logic used for the 2 different types of map images is different, hence using the data stored in variable map_type, we have separated out the 2 algorithms.

# In images containing Discrete Legends, the colour associated with the states must be one of the values associated to the legends, hence a simple
# Euclidean distance evaluation metric is suitable to calculate the value corresponding to each state.

# In images containing Colour Bar, the colour associated with the states could lie anywhere in the colour bar and hence, we leverage the piecewise linear
# interpolation method to obtain the value corresponding to each state.

if map_type == "Discrete Legends":
    print(map_type)
    for filename, state, state_color in data_a:
        min_distance = float('inf')
        assigned_value = None
        assigned_unit = None
        for file_name, map_type, map_title, color, average_value, unit in data_b:
            # calculating Euclidean distance
            distance = sum((c1 - c2) ** 2 for c1, c2 in zip(state_color, map_color))
            if distance < min_distance:
                min_distance = distance
                assigned_value = average_value
                assigned_unit = unit
        output_data.append((state, assigned_value, assigned_unit))

    print(output_data)

elif map_type == "Colour Bar":
    print(map_type)
    for state, state_color in data_a:
        assigned_value = 0
        for i in range(len(data_b) - 1):
            # Extract legend numbers, colors, and average values for the current and next entry
            legend_1, colour_1, value_1 = data_b[i][1], data_b[i][2], data_b[i][3]
            legend_2, colour_2, value_2 = data_b[i + 1][1], data_b[i + 1][2], data_b[i + 1][3]
            
            # Calculate alpha using the formula
            A_R = (state_color[0] - colour_2[0]) / (colour_1[0] - colour_2[0])
            A_G = (state_color[1] - colour_2[1]) / (colour_1[1] - colour_2[1])
            A_B = (state_color[2] - colour_2[2]) / (colour_1[2] - colour_2[2])

            A = (A_R + A_G + A_B)/3
            
            if 0<=A and A<=1:
                assigned_value = A*(value_1-value_2)+value_2
                # print(state, assigned_value)
        output_data.append((state, assigned_value, unit))

df[map_title]=""
for state, assigned_value, assigned_unit in output_data:
    df.loc[df.State_Name==state, map_title] = assigned_value
    print(df.loc[df.State_Name==state, map_title])
print(df)
df.to_csv('Result.csv',index = False)
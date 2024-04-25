# The input to this code is from segmentation of the map image and from the OCR data extraction.
# The segmentation input file containsthe type of map image(discrete or colour bar) followed by the states and their average colour value in RGB format.
# The OCR input file contains the Title of the map image along with the data present in the image - the values along with their
# corresponding colour value in RGB format.

import numpy as np
import pandas as pd

df = pd.read_csv('Result.csv')
# ocr_df = pd.read_csv("OCR_output.csv")
seg_df = pd.read_csv("Segmentation_output.csv")

map_type = ""
map_title = ""
map_name = ""

data_a = []
rows, cols = seg_df.shape

# iterating through each row and selecting
# 'Class Name' and 'RGB Colour' column respectively.
for row in seg_df.itertuples():
    file_name = row[1]
    state = row[2]
    color = row[6]
    data_a.append((file_name, state, color))

# # Function to perform piecewise linear interpolation on a given range.(Not used)
# def piecewise_linear_interpolation(C, V0, V1, C0, C1):
#     # Normalize RGB colors to the range [0, 1]
#     C_norm = np.array(C) / 255.0
#     C0_norm = np.array(C0) / 255.0
#     C1_norm = np.array(C1) / 255.0
    
#     # Calculate interpolated value using normalized colors
#     V_norm = V0 + (V1 - V0) * np.linalg.norm(C_norm - C0_norm) / np.linalg.norm(C1_norm - C0_norm)
    
#     # Reverse normalization to obtain final integer value
#     # V = int(round(V_norm))
#     V = V_norm
#     return V

# with open('Input_files/DLinput_from_segmentation.txt', 'r') as file_a:
#     map_type = file_a.readline().strip()
#     # print(map_type)
#     for line in file_a:
#         line = line.strip()[1:-1]  # Remove leading '[' and trailing ']'
#         parts = line.split(', ')
#         state = parts[0]
#         color = (int(parts[1]), int(parts[2]), int(parts[3]))
#         # print(color)
#         file_a_data.append((state, color))

# test code for Discrete Legends Input
# with open('Input_files/DLinput_from_segmentation.txt', 'r') as file_a:
#     map_type = file_a.readline().strip()
#     # print(map_type)
#     for line in file_a:
#         line = line.strip()[1:-1]  # Remove leading '[' and trailing ']'
#         parts = line.split(', ')
#         state = parts[0]
#         color = (int(parts[1]), int(parts[2]), int(parts[3]))
#         # print(color)
#         file_a_data.append((state, color))

# print(file_a_data)

# File B stores the data from the OCR input
# file_b_data = []
# with open('Input_files/test_OCR_output_DL.txt', 'r') as file_b:
#     map_title = file_b.readline().strip()
#     for line in file_b:
#         line = line.strip()[1:-1]  # Remove leading '[' and trailing ']'
#         parts = line.split(', ')
#         map_num = parts[0]
#         legend_num = int(parts[1])
#         color = (int(parts[2]),int(parts[3]),int(parts[4]))  # Evaluate the string representation of the list
#         # print(color)
#         if parts[5] != "'N/A'":
#             average_value = float(parts[5])
#         else:
#             average_value = -1
#         unit = parts[6]
#         # print(unit)
#         file_b_data.append((map_num, legend_num, color, average_value, unit))

# output_data = []
# print(file_b_data)


# Performing colour association/matching to assign values to each state present in the map image, hence preparing data for analysis.
# The logic used for the 2 different types of map images is different, hence using the data stored in variable map_type, we have separated out the 2 algorithms.

# In images containing Discrete Legends, the colour associated with the states must be one of the values associated to the legends, hence a simple
# Euclidean distance evaluation metric is suitable to calculate the value corresponding to each state.

# In images containing Colour Bar, the colour associated with the states could lie anywhere in the colour bar and hence, we leverage the piecewise linear
# interpolation method to obtain the value corresponding to each state.

# if map_type == "Discrete Legends":
#     print(map_type)
#     for state, state_color in file_a_data:
#         min_distance = float('inf')
#         assigned_value = None
#         assigned_unit = None
#         for map_num, legend_num, map_color, average_value, unit in file_b_data:
#             # calculatin Euclidean distance
#             distance = sum((c1 - c2) ** 2 for c1, c2 in zip(state_color, map_color))
#             if distance < min_distance:
#                 min_distance = distance
#                 assigned_value = average_value
#                 assigned_unit = unit
#         output_data.append((state, assigned_value, assigned_unit))

    # print(output_data)
    
#     with open('Output_files/DetectedValuesDL.txt', 'w') as output_file:
#         output_file.write(f"{map_title}\n")
#         for state, assigned_value, assigned_unit in output_data:
#             output_file.write(f"{state}: {assigned_value}, {assigned_unit}\n")

# elif map_type == "Colour Bar":
#     print(map_type)
#     for state, state_color in file_a_data:
#         assigned_value = 0
#         for i in range(len(file_b_data) - 1):
#             # Extract legend numbers, colors, and average values for the current and next entry
#             legend_1, colour_1, value_1 = file_b_data[i][1], file_b_data[i][2], file_b_data[i][3]
#             legend_2, colour_2, value_2 = file_b_data[i + 1][1], file_b_data[i + 1][2], file_b_data[i + 1][3]
            
#             # Calculate alpha using the formula
#             A_R = (state_color[0] - colour_2[0]) / (colour_1[0] - colour_2[0])
#             A_G = (state_color[1] - colour_2[1]) / (colour_1[1] - colour_2[1])
#             A_B = (state_color[2] - colour_2[2]) / (colour_1[2] - colour_2[2])

#             A = (A_R + A_G + A_B)/3
            
#             if 0<=A and A<=1:
#                 assigned_value = A*(value_1-value_2)+value_2
#                 # print(state, assigned_value)
#         output_data.append((state, assigned_value, unit))

#     # Write output to a file
#     # with open('Output_files/DetectedValuesCB.txt', 'w') as output_file:
#     #     output_file.write(f"{map_type}\n")
#     #     for state, assigned_value, assigned_unit in output_data:
#     #         output_file.write(f"{state}: {assigned_value}, {assigned_unit}\n")

# # for state, assigned_value, assigned_unit in output_data:

# df[map_title]=""
# for state, assigned_value, assigned_unit in output_data:
#     df.loc[df.State_Name==state, map_title] = assigned_value
#     print(df.loc[df.State_Name==state, map_title])
# print(df)
# df.to_csv('Result.csv',index = False)
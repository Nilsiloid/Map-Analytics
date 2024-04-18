# the input to this code is from segmentation of the map image.
# the input file contains states and their average colour value in RGB format.

# Discrete Legends -

import numpy as np

def piecewise_linear_interpolation(C, V0, V1, C0, C1):
    # Normalize RGB colors to the range [0, 1]
    C_norm = np.array(C) / 255.0
    C0_norm = np.array(C0) / 255.0
    C1_norm = np.array(C1) / 255.0
    
    # Calculate interpolated value using normalized colors
    V_norm = V0 + (V1 - V0) * np.linalg.norm(C_norm - C0_norm) / np.linalg.norm(C1_norm - C0_norm)
    
    # Reverse normalization to obtain final integer value
    # V = int(round(V_norm))
    V = V_norm
    return V

# Read File A
file_a_data = []
map_type = ""

with open('Input_files/CBinput_from_segmentation2.txt', 'r') as file_a:
    map_type = file_a.readline().strip()
    # print(map_type)
    for line in file_a:
        line = line.strip()[1:-1]  # Remove leading '[' and trailing ']'
        parts = line.split(', ')
        state = parts[0]
        color = (int(parts[1]), int(parts[2]), int(parts[3]))
        # print(color)
        file_a_data.append((state, color))

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

# Read File B
file_b_data = []
with open('Input_files/test_OCR_output_CB2.txt', 'r') as file_b:
    for line in file_b:
        line = line.strip()[1:-1]  # Remove leading '[' and trailing ']'
        parts = line.split(', ')
        map_num = parts[0]
        legend_num = int(parts[1])
        color = (int(parts[2]),int(parts[3]),int(parts[4]))  # Evaluate the string representation of the list
        # print(color)
        average_value = float(parts[5])
        unit = parts[6]
        file_b_data.append((map_num, legend_num, color, average_value, unit))

output_data = []
# print(file_b_data)
# Perform matching and assign values 
       
if map_type == "Discrete Legends":
    print(map_type)
    for state, state_color in file_a_data:
        min_distance = float('inf')
        assigned_value = None
        assigned_unit = None
        for map_num, legend_num, map_color, average_value, unit in file_b_data:
            distance = sum((c1 - c2) ** 2 for c1, c2 in zip(state_color, map_color))
            if distance < min_distance:
                min_distance = distance
                assigned_value = average_value
                assigned_unit = unit
        output_data.append((state, assigned_value, unit))
    
    with open('Output_files/DetectedValuesDL.txt', 'w') as output_file:
        # output_file.write(f"{map_type}\n")
        for state, assigned_value, assigned_unit in output_data:
            output_file.write(f"{state}: {assigned_value}, {assigned_unit}\n")

elif map_type == "Colour Bar":
    print(map_type)
    for state, state_color in file_a_data:
        assigned_value = -1
        for i in range(len(file_b_data) - 1):
            # Extract legend numbers, colors, and average values for the current and next entry
            legend_1, colour_1, value_1 = file_b_data[i][1], file_b_data[i][2], file_b_data[i][3]
            legend_2, colour_2, value_2 = file_b_data[i + 1][1], file_b_data[i + 1][2], file_b_data[i + 1][3]
            
            # Calculate alpha using the formula
            A_R = (state_color[0] - colour_2[0]) / (colour_1[0] - colour_2[0])
            A_G = (state_color[1] - colour_2[1]) / (colour_1[1] - colour_2[1])
            A_B = (state_color[2] - colour_2[2]) / (colour_1[2] - colour_2[2])

            A = (A_R + A_G + A_B)/3
            # print(A)
            if 0<=A and A<=1:
                assigned_value = A*(value_1-value_2)+value_2
                print(state, assigned_value)

            # print(assigned_value)
            # print("separator1")
        output_data.append((state, assigned_value, unit))
        # print("separator")

    # Write output to a file
    with open('Output_files/DetectedValuesCB.txt', 'w') as output_file:
        # output_file.write(f"{map_type}\n")
        for state, assigned_value, assigned_unit in output_data:
            output_file.write(f"{state}: {assigned_value}, {assigned_unit}\n")
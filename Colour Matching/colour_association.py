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

# Convert RGB to CMYK
def rgb_to_cmyk(r, g, b):
    r_new =  (r / 255.0)
    g_new =  (g / 255.0)
    b_new =  (b / 255.0)
    k = 1- max(r_new, g_new, b_new)
    if k == 1:  # Avoid division by zero
        c = m = y = 0
    else:
        c = (1 - r_new - k) / (1 - k)
        m = (1 - g_new - k) / (1 - k)
        y = (1 - b_new - k) / (1 - k)
    return c, m, y, k

# Read File A
file_a_data = []
map_type = ""

with open('input_from_segmentation.txt', 'r') as file_a:
    map_type = file_a.readline().strip()
    # print(map_type)
    for line in file_a:
        line = line.strip()[1:-1]  # Remove leading '[' and trailing ']'
        parts = line.split(', ')
        state = parts[0]
        color = (int(parts[1]), int(parts[2]), int(parts[3]))
        # print(color)
        file_a_data.append((state, color))

# print(file_a_data)

# Read File B
file_b_data = []
with open('PaddleOCR_output_test.txt', 'r') as file_b:
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
elif map_type == "Colour Bar":
    print(map_type)
    for state, state_color in file_a_data:
        assigned_value = -1
        for i in range(len(file_b_data) - 1):
            # Extract legend numbers, colors, and average values for the current and next entry
            legend_1, colour_1, value_1 = file_b_data[i][1], file_b_data[i][2], file_b_data[i][3]
            legend_2, colour_2, value_2 = file_b_data[i + 1][1], file_b_data[i + 1][2], file_b_data[i + 1][3]

            # V = piecewise_linear_interpolation(state_color, value_1, value_2, color_1, color_2)
            # print(V)
            # assigned_value = (assigned_value*(i) + V)/(i+1)

            c_state,m_state,y_state,k_state = rgb_to_cmyk(state_color[0], state_color[1], state_color[2])
            c_colour_1,m_colour_1,y_colour_1,k_colour_1 = rgb_to_cmyk(colour_1[0], colour_1[1], colour_1[2])
            c_colour_2,m_colour_2,y_colour_2,k_colour_2 = rgb_to_cmyk(colour_2[0], colour_2[1], colour_2[2])

            print(c_state, m_state, y_state, k_state)
            print(c_colour_1, m_colour_1, y_colour_1, k_colour_1)
            print(c_colour_2, m_colour_2, y_colour_2, k_colour_2)

            V_new_c = (c_state - c_colour_2) * (value_1 - value_2) / (c_colour_1 - c_colour_2) + value_1
            V_new_m = (m_state - m_colour_2) * (value_1 - value_2) / (m_colour_1 - m_colour_2) + value_1
            V_new_y = (y_state - y_colour_2) * (value_1 - value_2) / (y_colour_1 - y_colour_2) + value_1
            V_new_k = (k_state - k_colour_2) * (value_1 - value_2) / (k_colour_1 - k_colour_2) + value_1

            V_new = (V_new_c+V_new_m+V_new_y+V_new_k)/4
            assigned_value = (assigned_value*(i) + V_new)/(i+1)
            
            # Calculate V using the formula
            # V_new_R = (state_color[0] - color_2[0]) * (value_1 - value_2) / (color_1[0] - color_2[0]) + value_1
            # V_new_G = (state_color[1] - color_2[1]) * (value_1 - value_2) / (color_1[1] - color_2[1]) + value_1
            # V_new_B = (state_color[2] - color_2[2]) * (value_1 - value_2) / (color_1[2] - color_2[2]) + value_1

            # V_new = (0.33*V_new_R+0.59*V_new_G+0.11*V_new_B)
            # V_new = (V_new_R+V_new_G+V_new_B)/3
            # print(V_new_R, V_new_G, V_new_B, "----------", V_new)
            # assigned_value = (assigned_value*(i) + V_new)/(i+1)
            # print("separator1")
        output_data.append((state, assigned_value, unit))
        # print("separator")

# print(output_data)

# Write output to a file
with open('DetectedValuesCB.txt', 'w') as output_file:
    for state, assigned_value, assigned_unit in output_data:
        output_file.write(f"{state}: {assigned_value}, {assigned_unit}\n")


# # Read input file with state values
# def read_input_file(input_file):
#     state_data = []
#     with open(input_file, 'r') as file:
#         for line in file:
#             state, r, g, b = line.strip().split(',')
#             state_data.append((state, int(r), int(g), int(b)))
#     return state_data

# # Function to read RGB values from input file
# def read_rgb_values(input_file):
#     rgb_values = []
#     with open(input_file, 'r') as file:
#         for line in file:
#             # Split line and convert RGB values to integers
#             rgb = [int(x) for x in line.strip().split()]
#             rgb_values.append(rgb)
#     return rgb_values
        
# with open('input_from_segmentation.txt', 'r') as file_a:
#     for line in file_a:
#         line = line.strip()[1:-1]  # Remove leading '[' and trailing ']'
#         parts = line.split(', ')
#         state = parts[0]
#         color = eval(parts[1])  # Evaluate the string representation of the list
#         file_a_data.append((state, color))

# # Match RGB values with existing list
# def match_rgb_values(state_data, rgb_list):
#     matched_data = []
#     for state, r, g, b in state_data:
#         double_value = None
#         for rgb, value in rgb_list:
#             if rgb == (r, g, b):
#                 double_value = value * 2
#                 break
#         matched_data.append((state, double_value))
#     return matched_data

# # Write output to file
# def write_output_file(output_file, matched_data):
#     with open(output_file, 'w') as file:
#         for state, double_value in matched_data:
#             file.write(f'{state},{double_value}\n')

# # Main function
# def main(input_file, output_file):
#     # List of RGB values and corresponding double values
#     rgb_list = [
#         ((255, 0, 0), 10),
#         ((0, 255, 0), 20),
#         ((0, 0, 255), 30),
#     ]

#     # Read input file
#     state_data = read_input_file(input_file)

#     input_file = 'rgb_values.txt'  # Replace with your input file path
#     rgb_list = read_rgb_values(input_file)

#     # Match RGB values with existing list
#     matched_data = match_rgb_values(state_data, rgb_list)

#     # Write output to file
#     write_output_file(output_file, matched_data)

# # Example usage:
# input_file = 'input_from_segmentation.txt'  # Replace with your input file path
# output_file = 'output.txt'  # Replace with your output file path
# main(input_file, output_file)

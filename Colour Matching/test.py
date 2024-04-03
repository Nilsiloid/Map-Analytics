import numpy as np

def piecewise_linear_interpolation(C, V0, V1, C0, C1):
    # Normalize RGB colors to the range [0, 1]
    C_norm = np.array(C) / 255.0
    C0_norm = np.array(C0) / 255.0
    C1_norm = np.array(C1) / 255.0
    
    # Calculate interpolated value using normalized colors
    V_norm = V0 + (V1 - V0) * np.linalg.norm(C_norm - C0_norm) / np.linalg.norm(C1_norm - C0_norm)
    
    # Reverse normalization to obtain final integer value
    V = int(round(V_norm))
    return V

# Example usage
C = [100, 50, 150]  # RGB color
V0 = 0  # Initial value
V1 = 255  # Final value
C0 = [50, 25, 100]  # RGB color corresponding to initial value
C1 = [150, 75, 200]  # RGB color corresponding to final value

V = piecewise_linear_interpolation(C, V0, V1, C0, C1)
print("Interpolated value:", V)

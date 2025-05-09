import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm  # Import tqdm for the progress bar

# Parameters
nx, ny = 400, 200  # Grid size
viscosity = 0.02  # Kinematic viscosity
u_inlet = 0.1  # Inlet velocity
tau = 3 * viscosity + 0.5  # Relaxation time
omega = 1 / tau  # Relaxation parameter
naca_number = '0012'  # NACA airfoil (e.g., NACA 0012)
angle_of_attack = 10  # Angle of attack in degrees

# Convert angle of attack to radians
aoa = np.radians(angle_of_attack)

# Lattice weights and velocities
weights = np.array([4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36])
cx = np.array([0, 1, 0, -1, 0, 1, -1, -1, 1])
cy = np.array([0, 0, 1, 0, -1, 1, 1, -1, -1])

# Initialize distribution functions
f = np.ones((ny, nx, 9))  # Distribution function
feq = np.zeros_like(f)  # Equilibrium distribution function
rho = np.ones((ny, nx))  # Density
ux = np.zeros((ny, nx))  # Velocity x-component
uy = np.zeros((ny, nx))  # Velocity y-component

# Define the NACA airfoil
def naca_airfoil(x, naca=naca_number):
    """Returns the y-coordinates of the upper and lower surfaces of a NACA airfoil."""
    t = float(naca[2:]) / 100  # Thickness
    yt = 5 * t * (0.2969 * np.sqrt(np.maximum(x, 0)) - 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1015 * x**4)
    return yt, -yt

# Create a mask for the airfoil
def create_airfoil_mask(nx, ny, aoa):
    """Create a mask for the NACA airfoil at an angle of attack."""
    mask = np.zeros((ny, nx), dtype=bool)
    x_airfoil = np.linspace(0, 1, nx)
    y_upper, y_lower = naca_airfoil(x_airfoil)

    # Rotate the airfoil
    x_rot = (x_airfoil - 0.5) * np.cos(aoa) - (y_upper - 0.5) * np.sin(aoa) + 0.5
    y_rot = (x_airfoil - 0.5) * np.sin(aoa) + (y_upper - 0.5) * np.cos(aoa) + 0.5

    # Scale and shift to grid coordinates
    x_idx = np.clip((x_rot * nx).astype(int), 0, nx - 1)
    y_idx = np.clip((y_rot * ny).astype(int), 0, ny - 1)
    mask[y_idx, x_idx] = True
    return mask

airfoil_mask = create_airfoil_mask(nx, ny, aoa)

# Main simulation loop with tqdm progress bar
n_steps = 10000  # Total number of steps
for step in tqdm(range(n_steps), desc="Simulating", unit="step"):
    # Compute macroscopic variables
    rho = np.sum(f, axis=2)
    rho = np.clip(rho, 1e-10, None)  # Avoid division by zero
    ux = np.sum(f * cx, axis=2) / rho
    uy = np.sum(f * cy, axis=2) / rho

    # Apply boundary conditions (inlet velocity)
    ux[:, 0] = u_inlet
    uy[:, 0] = 0

    # Compute equilibrium distribution function
    for i in range(9):
        cu = 3 * (cx[i] * ux + cy[i] * uy)
        feq[:, :, i] = rho * weights[i] * (1 + cu + 0.5 * cu**2 - 1.5 * (ux**2 + uy**2))

    # Collision step
    f -= omega * (f - feq)

    # Streaming step
    for i in range(9):
        f[:, :, i] = np.roll(f[:, :, i], (cy[i], cx[i]), axis=(0, 1))

    # Bounce-back boundary conditions for the airfoil
    for i in range(9):
        f[airfoil_mask, i] = f[airfoil_mask, 8 - i]

    # Clamp values to avoid overflow
    f = np.clip(f, -1e10, 1e10)

# Final visualization of the flow
velocity_magnitude = np.sqrt(ux**2 + uy**2)

# Plot the final state
plt.figure(figsize=(10, 5))
plt.imshow(velocity_magnitude, cmap='jet', origin='lower')
plt.colorbar(label='Velocity Magnitude')
plt.title('Final Flow Around Airfoil')
plt.xlabel('x')
plt.ylabel('y')

# Overlay the airfoil shape
x_airfoil = np.linspace(0, 1, nx)
y_upper, y_lower = naca_airfoil(x_airfoil)
x_rot = (x_airfoil - 0.5) * np.cos(aoa) - (y_upper - 0.5) * np.sin(aoa) + 0.5
y_rot = (x_airfoil - 0.5) * np.sin(aoa) + (y_upper - 0.5) * np.cos(aoa) + 0.5
plt.fill_between(x_rot * nx, y_rot * ny, color='gray', alpha=0.5)  # Rotated airfoil

plt.tight_layout()
plt.show()
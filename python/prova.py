import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # For 3D trajectory

def calculate_trajectory(initial_pos, initial_vel, g=9.81, time_step=0.1, total_time=10):
    """
    Calculate the trajectory of an object under constant gravity.
    """
    time_points = np.arange(0, total_time, time_step)
    x0, y0, z0 = initial_pos
    vx0, vy0, vz0 = initial_vel
    
    x_pos = x0 + vx0 * time_points
    y_pos = y0 + vy0 * time_points
    z_pos = z0 + vz0 * time_points - 0.5 * g * time_points**2
    
    return time_points, x_pos, y_pos, z_pos

def plot_trajectory_2d(time_points, x_pos, y_pos, z_pos, save_path=None):
    """Plot 2D views of the trajectory and save to file"""
    plt.figure(figsize=(15, 5))
    
    # XY view
    plt.subplot(1, 3, 1)
    plt.plot(x_pos, y_pos)
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.title('XY Plane Trajectory')
    plt.grid(True)
    
    # XZ view (side view)
    plt.subplot(1, 3, 2)
    plt.plot(x_pos, z_pos)
    plt.xlabel('X Position (m)')
    plt.ylabel('Z Position (m)')
    plt.title('XZ Plane Trajectory (Side View)')
    plt.grid(True)
    
    # YZ view (front view)
    plt.subplot(1, 3, 3)
    plt.plot(y_pos, z_pos)
    plt.xlabel('Y Position (m)')
    plt.ylabel('Z Position (m)')
    plt.title('YZ Plane Trajectory (Front View)')
    plt.grid(True)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_trajectory_3d(time_points, x_pos, y_pos, z_pos, save_path=None):
    """Plot a 3D trajectory and save to file"""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot(x_pos, y_pos, z_pos, label='Trajectory')
    ax.scatter(x_pos[0], y_pos[0], z_pos[0], color='red', label='Start')
    ax.scatter(x_pos[-1], y_pos[-1], z_pos[-1], color='green', label='End')
    
    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Y Position (m)')
    ax.set_zlabel('Z Position (m)')
    ax.set_title('3D Trajectory')
    ax.legend()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def main(save_to_files=False):
    # Example initial conditions
    initial_position = [0, 0, 0]  # x, y, z in meters
    initial_velocity = [10, 5, 20]  # vx, vy, vz in m/s
    
    # Calculate trajectory
    time, x, y, z = calculate_trajectory(initial_position, initial_velocity)
    
    # Plot results
    if save_to_files:
        plot_trajectory_2d(time, x, y, z, save_path='2d_trajectory_views.png')
        plot_trajectory_3d(time, x, y, z, save_path='3d_trajectory.png')
        print("Plots saved as:")
        print("- 2d_trajectory_views.png")
        print("- 3d_trajectory.png")
    else:
        plot_trajectory_2d(time, x, y, z)
        plot_trajectory_3d(time, x, y, z)

if __name__ == "__main__":
    # Set save_to_files=True to save plots instead of showing them
    main(save_to_files=True)
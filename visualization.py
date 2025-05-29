import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from typing import Dict, List
import numpy as np
from waypoints import DroneTrajectory

class VisualizationSystem:
    """Handles 3D/4D visualization of trajectories and conflicts"""
    
    @staticmethod
    def plot_3d_trajectories(trajectories: Dict[str, DroneTrajectory], 
                            conflicts: List[Dict] = None):
        """Create 3D plot of all trajectories with conflict markers"""
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot each trajectory
        for drone_id, traj in trajectories.items():
            data = traj.get_full_trajectory()
            ax.plot(data['x'], data['y'], data['z'], 
                   label=drone_id, alpha=0.7)
            
            # Mark start and end points
            ax.scatter(data['x'][0], data['y'][0], data['z'][0], 
                      marker='o', s=50, label=f'{drone_id} Start')
            ax.scatter(data['x'][-1], data['y'][-1], data['z'][-1], 
                      marker='x', s=50, label=f'{drone_id} End')
        
        # Highlight conflicts
        if conflicts:
            for conflict in conflicts:
                pos = conflict['primary_position']
                ax.scatter(pos[0], pos[1], pos[2], 
                          c='red', s=100, marker='*',
                          label=f"Conflict with {conflict['conflicting_drone']}")
        
        ax.set_xlabel('X Position (m)')
        ax.set_ylabel('Y Position (m)')
        ax.set_zlabel('Altitude (m)')
        ax.set_title('Drone Trajectories in 3D Space')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def animate_4d_trajectories(trajectories: Dict[str, DroneTrajectory],
                               conflicts: List[Dict] = None,
                               interval: int = 100):
        """Create animated 4D (3D + time) visualization"""
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Prepare trajectory data
        all_data = {}
        time_points = set()
        for drone_id, traj in trajectories.items():
            data = traj.get_full_trajectory(time_step=0.5)
            all_data[drone_id] = data
            time_points.update(data['times'])
        
        sorted_times = sorted(time_points)
        min_time, max_time = sorted_times[0], sorted_times[-1]
        
        # Initialize plot elements
        lines = {drone_id: ax.plot([], [], [], label=drone_id)[0] 
                for drone_id in trajectories}
        points = {drone_id: ax.plot([], [], [], 'o')[0] 
                 for drone_id in trajectories}
        conflict_markers = ax.plot([], [], [], 'r*', markersize=10)[0]
        
        # Set axis limits
        all_x = np.concatenate([data['x'] for data in all_data.values()])
        all_y = np.concatenate([data['y'] for data in all_data.values()])
        all_z = np.concatenate([data['z'] for data in all_data.values()])
        
        ax.set_xlim(min(all_x)-10, max(all_x)+10)
        ax.set_ylim(min(all_y)-10, max(all_y)+10)
        ax.set_zlim(min(all_z)-10, max(all_z)+10)
        
        ax.set_xlabel('X Position (m)')
        ax.set_ylabel('Y Position (m)')
        ax.set_zlabel('Altitude (m)')
        ax.set_title('4D Drone Trajectories (3D Space + Time)')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        def update(frame):
            current_time = sorted_times[frame]
            time_text = f"Time: {current_time.strftime('%H:%M:%S')}"
            
            # Update each drone's position
            for drone_id, data in all_data.items():
                mask = [t <= current_time for t in data['times']]
                x = data['x'][mask]
                y = data['y'][mask]
                z = data['z'][mask]
                
                lines[drone_id].set_data(x, y)
                lines[drone_id].set_3d_properties(z)
                
                if len(x) > 0:
                    points[drone_id].set_data([x[-1]], [y[-1]])
                    points[drone_id].set_3d_properties([z[-1]])
            
            # Show conflicts if they exist at this time
            if conflicts:
                current_conflicts = [c for c in conflicts if c['time'] == current_time]
                if current_conflicts:
                    conflict_x = [c['primary_position'][0] for c in current_conflicts]
                    conflict_y = [c['primary_position'][1] for c in current_conflicts]
                    conflict_z = [c['primary_position'][2] for c in current_conflicts]
                    
                    conflict_markers.set_data(conflict_x, conflict_y)
                    conflict_markers.set_3d_properties(conflict_z)
                else:
                    conflict_markers.set_data([], [])
                    conflict_markers.set_3d_properties([])
            
            ax.set_title(f'4D Drone Trajectories\n{time_text}')
            return list(lines.values()) + list(points.values()) + [conflict_markers]
        
        ani = FuncAnimation(fig, update, frames=len(sorted_times),
                          interval=interval, blit=True)
        plt.tight_layout()
        plt.show()
        return ani
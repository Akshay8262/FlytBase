from typing import Dict, List
from datetime import datetime, timedelta
import math
from waypoints import DroneTrajectory

class DeconflictionEngine:
    """Core conflict detection engine with 4D spatiotemporal checks"""
    
    def __init__(self, safety_buffer: float = 10.0):
        self.safety_buffer = safety_buffer
        self.trajectories = {}
    
    def add_trajectory(self, trajectory: DroneTrajectory):
        """Register a drone trajectory with the system"""
        self.trajectories[trajectory.drone_id] = trajectory
    
    def check_conflicts(self, primary_id: str, 
                       time_step: float = 1.0) -> Dict:
        """Check for conflicts between primary trajectory and all others"""
        if primary_id not in self.trajectories:
            raise ValueError(f"Unknown drone ID: {primary_id}")
        
        primary = self.trajectories[primary_id]
        conflicts = []
        
        # Check against all other trajectories
        for drone_id, trajectory in self.trajectories.items():
            if drone_id == primary_id:
                continue
            
            # Find overlapping time window
            overlap_start = max(primary.start_time, trajectory.start_time)
            overlap_end = min(primary.end_time, trajectory.end_time)
            
            if overlap_start >= overlap_end:
                continue  # No temporal overlap
                
            # Check at regular time intervals
            current_time = overlap_start
            while current_time <= overlap_end:
                pos1 = primary.get_position_at_time(current_time)
                pos2 = trajectory.get_position_at_time(current_time)
                
                distance = math.sqrt(
                    (pos1[0]-pos2[0])**2 + 
                    (pos1[1]-pos2[1])**2 + 
                    (pos1[2]-pos2[2])**2
                )
                
                if distance < self.safety_buffer:
                    conflicts.append({
                        'time': current_time,
                        'primary_position': pos1,
                        'conflicting_drone': drone_id,
                        'conflicting_position': pos2,
                        'distance': distance
                    })
                
                current_time += timedelta(seconds=time_step)
        
        return {
            'primary_drone': primary_id,
            'status': 'clear' if not conflicts else 'conflict',
            'conflicts': conflicts,
            'safety_buffer': self.safety_buffer
        }
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Tuple
import numpy as np
from scipy.interpolate import interp1d
import math

@dataclass
class Waypoint:
    x: float
    y: float
    z: float = 0.0
    timestamp: Optional[datetime] = None

class DroneTrajectory:
    """Represents a drone's trajectory with 4D (x,y,z,t) waypoints"""
    
    def __init__(self, drone_id: str, waypoints: List[Waypoint]):
        self.drone_id = drone_id
        self.waypoints = sorted(waypoints, key=lambda wp: wp.timestamp)
        self.start_time = self.waypoints[0].timestamp
        self.end_time = self.waypoints[-1].timestamp
        self._create_interpolators()
    
    def _create_interpolators(self):
        """Create interpolation functions for each dimension"""
        times = self._get_relative_times()
        x = [wp.x for wp in self.waypoints]
        y = [wp.y for wp in self.waypoints]
        z = [wp.z for wp in self.waypoints]
        
        self.x_interp = interp1d(times, x, kind='linear', fill_value='extrapolate')
        self.y_interp = interp1d(times, y, kind='linear', fill_value='extrapolate')
        self.z_interp = interp1d(times, z, kind='linear', fill_value='extrapolate')
    
    def _get_relative_times(self) -> np.ndarray:
        """Convert absolute timestamps to relative seconds from start"""
        return np.array([(wp.timestamp - self.start_time).total_seconds() 
                        for wp in self.waypoints])
    
    def get_position_at_time(self, time: datetime) -> Tuple[float, float, float]:
        """Get 3D position at specific time"""
        elapsed = (time - self.start_time).total_seconds()
        return (
            float(self.x_interp(elapsed)),
            float(self.y_interp(elapsed)),
            float(self.z_interp(elapsed))
        )
    
    def get_full_trajectory(self, time_step: float = 1.0) -> Dict:
        """Get complete trajectory at regular time intervals"""
        times = np.arange(0, (self.end_time - self.start_time).total_seconds(), time_step)
        return {
            'times': [self.start_time + timedelta(seconds=t) for t in times],
            'x': self.x_interp(times),
            'y': self.y_interp(times),
            'z': self.z_interp(times)
        }
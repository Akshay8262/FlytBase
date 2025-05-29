from datetime import datetime, timedelta
from typing import Dict, List
from waypoints import Waypoint, DroneTrajectory

def create_sample_mission() -> Dict[str, DroneTrajectory]:
    """Create sample mission with potential conflicts"""
    base_time = datetime.now()
    
    # Primary mission (drone1)
    primary_waypoints = [
        Waypoint(0, 0, 10, base_time + timedelta(seconds=0)),
        Waypoint(100, 100, 20, base_time + timedelta(seconds=60)),
        Waypoint(200, 0, 10, base_time + timedelta(seconds=120))
    ]
    
    # Other drones
    drone2_waypoints = [
        Waypoint(0, 100, 15, base_time + timedelta(seconds=30)),
        Waypoint(150, 50, 25, base_time + timedelta(seconds=90)),
        Waypoint(200, 100, 15, base_time + timedelta(seconds=150))
    ]
    
    drone3_waypoints = [
        Waypoint(50, 50, 30, base_time + timedelta(seconds=0)),
        Waypoint(50, 50, 10, base_time + timedelta(seconds=60)),
        Waypoint(50, 50, 30, base_time + timedelta(seconds=120))
    ]
    
    return {
        'drone1': DroneTrajectory('drone1', primary_waypoints),
        'drone2': DroneTrajectory('drone2', drone2_waypoints),
        'drone3': DroneTrajectory('drone3', drone3_waypoints)
    }
from deconfliction import DeconflictionEngine
from visualization import VisualizationSystem
from mission import create_sample_mission

def main():
    # Initialize systems
    deconfliction = DeconflictionEngine(safety_buffer=15.0)
    viz = VisualizationSystem()
    
    # Create and register trajectories
    trajectories = create_sample_mission()
    for drone_id, traj in trajectories.items():
        deconfliction.add_trajectory(traj)
    
    # Check for conflicts with primary drone (drone1)
    result = deconfliction.check_conflicts('drone1')
    
    # Print results
    print("\n=== Conflict Detection Results ===")
    print(f"Primary Drone: {result['primary_drone']}")
    print(f"Status: {result['status'].upper()}")
    print(f"Safety Buffer: {result['safety_buffer']} meters")
    
    if result['conflicts']:
        print("\nDetected Conflicts:")
        for i, conflict in enumerate(result['conflicts'], 1):
            print(f"\nConflict #{i}:")
            print(f"Time: {conflict['time'].strftime('%H:%M:%S')}")
            print(f"Primary Position: {conflict['primary_position']}")
            print(f"With Drone: {conflict['conflicting_drone']}")
            print(f"Conflict Position: {conflict['conflicting_position']}")
            print(f"Distance: {conflict['distance']:.2f} meters")
    else:
        print("\nNo conflicts detected!")
    
    # Visualize
    print("\nGenerating visualizations...")
    viz.plot_3d_trajectories(trajectories, result['conflicts'])
    print("Generating 4D animation...")
    viz.animate_4d_trajectories(trajectories, result['conflicts'])

if __name__ == "__main__":
    main()
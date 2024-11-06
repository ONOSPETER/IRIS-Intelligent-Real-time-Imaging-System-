import json
import math

class GraphModule:
    def __init__(self, camera_json, graph_json, map_file):
        # Load JSON files for camera mapping, graph structure, and map layout
        with open(camera_json, 'r') as f:
            self.cameras = json.load(f)
        with open(graph_json, 'r') as f:
            self.graph = json.load(f)
        with open(map_file, 'r') as f:
            self.map_data = json.load(f)
    
    def translate_location(self, camera_id, direction):
        """
        Translate target's location and direction into geographical coordinates.
        
        Parameters:
        - camera_id: The ID of the current camera observing the target
        - direction: The target's direction (e.g., 'left', 'right', 'front', 'behind')
        
        Returns:
        - Geographic coordinates of the new location as a tuple (latitude, longitude)
        """
        camera_data = self.cameras.get(camera_id, None)
        if not camera_data:
            print(f"No data found for camera ID: {camera_id}")
            return None
        
        # Get coordinates of the current camera
        current_coords = camera_data["coordinates"]
        
        # Use mapping data to find the exact geographical location in the direction
        if direction in camera_data["directions"]:
            location_name = camera_data["directions"][direction]
            return self.map_data.get(location_name, current_coords)
        else:
            print(f"Invalid direction '{direction}' for camera {camera_id}")
            return current_coords

    def calculate_next_camera(self, current_camera_id, target_direction):
        """
        Calculate the next best camera based on the target's movement and current position.
        
        Parameters:
        - current_camera_id: ID of the current camera observing the target
        - target_direction: Direction of target's movement
        
        Returns:
        - The ID of the best next camera
        """
        # Initialize variables to store the closest camera and its distance
        best_camera_id = None
        min_distance = float('inf')
        
        # Retrieve neighbor cameras from the graph structure
        neighbors = self.graph.get(current_camera_id, {}).get("neighbors", {})
        
        for neighbor_id, info in neighbors.items():
            # Check if this camera’s direction aligns with the target’s direction
            if info["direction"] == target_direction:
                # Calculate the shortest path (or distance) to the neighbor camera
                distance = info["distance"]
                if distance < min_distance:
                    min_distance = distance
                    best_camera_id = neighbor_id
        
        return best_camera_id if best_camera_id else current_camera_id

    def get_target_geolocation(self, camera_id, target_direction):
        """
        Provides a complete translation of the target’s position and likely next camera.
        
        Parameters:
        - camera_id: The current camera's ID
        - target_direction: The target's movement direction (e.g., 'left', 'right')
        
        Returns:
        - Dictionary containing the geographic coordinates and next camera ID
        """
        # Translate location to geographic coordinates
        geographic_coords = self.translate_location(camera_id, target_direction)
        
        # Calculate the best next camera
        next_camera_id = self.calculate_next_camera(camera_id, target_direction)
        
        return {
            "current_coordinates": geographic_coords,
            "next_camera_id": next_camera_id
        }

# Example usage:
# graph_module = GraphModule("camera.json", "graph.json", "map.json")
# target_info = graph_module.get_target_geolocation("cameraA", "right")
# print(target_info)

import cv2
import json

class Feed:
    def __init__(self, config_file):
        """
        Initializes the Feed module, loading camera and API configuration.
        """
        # Load configuration data from JSON file
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        self.api_key = self.config['api_key']  # API key if needed
        self.cameras = self.config['cameras']  # List of camera configurations

    def get_camera_feed(self, camera_id):
        """
        Retrieves the video feed for the given camera ID.
        """
        # Find camera details based on camera_id
        camera_info = next((cam for cam in self.cameras if cam['id'] == camera_id), None)
        
        if not camera_info:
            print(f"Camera with ID {camera_id} not found.")
            return None

        # Retrieve camera feed using its URL or source
        camera_url = camera_info['url']
        cap = cv2.VideoCapture(camera_url)
        
        if not cap.isOpened():
            print(f"Unable to access camera feed for ID {camera_id}.")
            return None

        return cap

    def release_camera(self, cap):
        """
        Releases the camera feed.
        """
        cap.release()

# Configuration file format (config.json):
# {
#   "api_key": "YOUR_API_KEY",
#   "cameras": [
#       {"id": "camera_1", "url": "http://your_camera_1_url"},
#       {"id": "camera_2", "url": "http://your_camera_2_url"},
#       ...
#   ]
# }

# Example usage
if __name__ == "__main__":
    feed = Feed("config.json")
    
    # Retrieve feed from a specific camera ID
    camera_id = "camera_1"
    cap = feed.get_camera_feed(camera_id)
    
    if cap:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Unable to retrieve frame.")
                break
            
            # Display the frame (optional)
            cv2.imshow("Camera Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Release the camera when done
        feed.release_camera(cap)
        cv2.destroyAllWindows()

import time
# Importing the necessary modules from the 'module' folder
from module.eye_module import EyeModule
from module.feed_module import FeedModule
from module.graph_module import GraphModule

class IRIS:
    def __init__(self, camera_config, graph_config, map_file):
        # Initialize EYE, Graph, and Feed modules
        self.eye = EYE()
        self.graph = GraphModule(camera_config, graph_config, map_file)
        self.feed = FeedModule(camera_config)
        
        # Initialize variables for tracking
        self.tracking_target = False
        self.current_camera_id = None
        self.marked_target = None

    def display_camera_feed(self, camera_id):
        """
        Display the camera feed for the specified camera.
        """
        print(f"\nDisplaying feed for Camera {camera_id}")
        frame = self.feed.get_camera_feed(camera_id)
        self.eye.process_frame(frame)
        print("Feed displayed successfully!\n")

    def mark_target(self, camera_id):
        """
        Mark a target on a specified camera feed and start tracking it.
        """
        frame = self.feed.get_camera_feed(camera_id)
        print("Please draw a bounding box around the target.")
        
        # User marks the target
        self.eye.set_target(frame)
        self.marked_target = camera_id
        self.tracking_target = True
        self.current_camera_id = camera_id
        print(f"Target marked on Camera {camera_id} and tracking initiated.")

    def disengage_tracking(self):
        """
        Disengage tracking of the current target.
        """
        self.tracking_target = False
        self.marked_target = None
        self.current_camera_id = None
        print("Tracking disengaged successfully.")

    def follow_target(self):
        """
        Follow the marked target, adjusting to the next best camera based on the target's movement.
        """
        if not self.tracking_target or not self.marked_target:
            print("No target is currently marked for tracking.")
            return

        print("Following target...")
        while self.tracking_target:
            frame = self.feed.get_camera_feed(self.current_camera_id)
            target_info = self.eye.process_frame(frame)

            # If movement detected, calculate next best camera
            next_camera_id = self.graph.calculate_next_camera(self.current_camera_id, target_info['direction'])
            if next_camera_id != self.current_camera_id:
                print(f"Switching to Camera {next_camera_id} based on target movement.")
                self.current_camera_id = next_camera_id
            else:
                print(f"Target remains in Camera {self.current_camera_id}")

            # Brief pause to simulate real-time tracking
            time.sleep(1)

    def menu(self):
        """
        CLI menu for user interaction.
        """
        while True:
            print("\n=== IRIS System Menu ===")
            print("1. Display camera feed")
            print("2. Mark a target and follow")
            print("3. Disengage tracking")
            print("4. Exit")
            choice = input("Select an option (1-4): ")

            if choice == "1":
                camera_id = input("Enter Camera ID to display feed: ")
                self.display_camera_feed(camera_id)

            elif choice == "2":
                camera_id = input("Enter Camera ID to mark target: ")
                self.mark_target(camera_id)
                self.follow_target()

            elif choice == "3":
                self.disengage_tracking()

            elif choice == "4":
                print("Exiting IRIS system.")
                break

            else:
                print("Invalid choice. Please select an option from the menu.")

# Example usage:
# iris = IRIS("camera_config.json", "graph_config.json", "map.json")
# iris.menu()

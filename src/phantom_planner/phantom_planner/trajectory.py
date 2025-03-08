import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import math

class CircularTrajectoryController(Node):
    def __init__(self):
        super().__init__('circular_trajectory_controller')

        # Create a publisher for joint velocity commands
        self.joint_velocity_publisher = self.create_publisher(Float64MultiArray, '/position_controller/commands', 10)

        # Timer to periodically send the joint velocities
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz
        self.angle = 0.0  # Initial angle for the circular trajectory

        self.radius = 0.2  # Radius of the circle (in meters, adjust accordingly)
        self.angular_velocity = 0.2  # Angular velocity in radians per second
        self.joint_velocities = [0.0, 0.0, 0.0, 0.0]  # Initialize joint velocities for 4 joints

    def timer_callback(self):
        """Callback function that runs periodically to send joint velocities."""
        self.send_circular_trajectory_velocity()

    def send_circular_trajectory_velocity(self):
        """Send joint velocity commands to simulate a circular trajectory for a 4-DOF arm."""
        # Calculate the joint velocities that will produce a circular motion.
        # For simplicity, let's assume a circular trajectory where all joints move with the same velocity.
        self.angle += self.angular_velocity * 0.1  # Increment angle (0.1 is the time step)

        # In this case, we will control the angular velocities of all joints uniformly for simplicity.
        # You could calculate more complex circular motions for each joint depending on your model.
        
        joint_velocity_1 = self.angular_velocity  # Joint 1 velocity (e.g., base rotation)
        joint_velocity_2 = self.angular_velocity  # Joint 2 velocity (e.g., shoulder movement)
        joint_velocity_3 = self.angular_velocity  # Joint 3 velocity (e.g., elbow movement)
        joint_velocity_4 = self.angular_velocity  # Joint 4 velocity (e.g., wrist movement)

        # Store the velocities in a Float64MultiArray message
        joint_velocity_msg = Float64MultiArray()
        joint_velocity_msg.data = [joint_velocity_1, joint_velocity_2, joint_velocity_3, joint_velocity_4]

        # Publish the velocity command to the position controller
        self.joint_velocity_publisher.publish(joint_velocity_msg)
        
        self.get_logger().info(f"Publishing joint velocities: {joint_velocity_1}, {joint_velocity_2}, {joint_velocity_3}, {joint_velocity_4}")

def main(args=None):
    rclpy.init(args=args)

    circular_trajectory_controller = CircularTrajectoryController()

    rclpy.spin(circular_trajectory_controller)

    circular_trajectory_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

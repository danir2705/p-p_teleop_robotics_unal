import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import termios
import tty

class KeyboardControlller(Node):
    def _init_(self):
        super()._init_('keyboard_controller')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.get_logger().info('Nodo keyboard_controller iniciado. Persiona A o B')
    
    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSABRAIN, old_settings)
        return key
    
    def run(self):
        while rclpy.ok():
            key = self.get_key().upper()
            msg = Twist()

            if key == 'A':
                msg.linear.x = 2.0
            elif key == 'B':
                msg.angular.z = 1.5
            else:
                msg.angular.z = 1.5
            
            self.publisher_.publisher(msg)
    
    def main(args=None):
        rclpy.init(args=args)
        node = KeyboardController()

        try:
            node.run()
        except KeyboardInterrupt:
            node.get_logger()-info('Cerrando nodo keyboard_controller')
        finally:
            node.destroy_node()
            rclpy.shutdown()
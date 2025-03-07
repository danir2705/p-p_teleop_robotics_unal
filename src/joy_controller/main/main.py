import rclpy
from rclpy.node import Node
import os
import time 
import pprint
import pygame
from std_msgs.msg import Float64, Float32MultiArray



class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        print(pygame.joystick.Joystick(0))

        self.controller.init()

    def listen(self):
        """Listen for events to happen"""
        
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)



class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Float32MultiArray, 'topic', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

        # Validacion de cconstruccion 
        self.controller = PS4Controller() 
        self.controller.init()
        self.controller.listen()

        print("Joy controlle init :D ")

        
    

    def timer_callback(self):
        dx, dy = 0.0    , 0.0
        for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.controller.axis_data[event.axis] = float(event.value)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.controller.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.controller.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.controller.hat_data[event.hat] = event.value


        if 0 < len(self.controller.axis_data.values()):
            dx = float(self.controller.axis_data.get("0"))
            dy = float(self.controller.axis_data.get("1"))
        
        print("dx : {} - dy: {}".format(dx, dy))
        

        msg = Float32MultiArray()

        msg.data = [dx, dy]

        self.publisher_.publish(msg)










def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
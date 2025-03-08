import rclpy
import os
import time 
import pprint
import pygame

from .PS4Controller import PS4Controller
import rclpy.logging
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
from rclpy.node import Node


class PhantomJoy(Node):

    def __init__(self):
        super().__init__('phantom_joy')

       # Publishers 
        self.twist_publisher_ = self.create_publisher(Twist, 'joy_vel', 10)
        self.mode_publisher_ = self.create_publisher(Bool, 'operation_mode', 10)

        
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

        # Validacion de cconstruccion 
        self.controller = PS4Controller() 
        try: 
            self.controller.init()
        except: 
            self.get_logger().info("No controller detected!")

        self.controller.listen()
        self.get_logger().info('node init. Continue to update state')

        self.operation_mode = False  # 0 - Manual, 1 - Auto 

    def timer_callback(self):
        self.controller.update() # Get all data
        dX = self.controller.get_axis() # Effector movement 
        
        """
            0 - X button
            1 - Circle button 
        """
        x_button = self.controller.get_button(self.controller.X_BUTTON)
        c_button  = self.controller.get_button(self.controller.C_BUTTON)

        if (x_button and not self.operation_mode):
            self.operation_mode = True
        elif (c_button and self.operation_mode): 
            self.operation_mode = False 


        # self.get_logger().info("Button: %d" % (self.operation_mode))
        

        twist_cmd = Twist() 
        operation_mode = Bool()

        # self.get_logger().info("dx: %f dy: %f dz: %f" % (dX[0], dX[1], dX[2]))

        # Twist packaging - Velocities from controller 
        twist_cmd.linear.x = dX[0]
        twist_cmd.linear.y = dX[1]
        twist_cmd.linear.z = dX[2]

        operation_mode.data = self.operation_mode

        # Publish information 
        self.twist_publisher_.publish(twist_cmd)
        self.mode_publisher_.publish(operation_mode)



        



def main(args=None):
    rclpy.init(args=args)

    phantom_joy = PhantomJoy()

    rclpy.spin(phantom_joy)

    phantom_joy.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
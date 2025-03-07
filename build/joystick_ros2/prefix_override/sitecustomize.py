import sys
if sys.prefix == 'C:\\Users\\yeira\\miniforge3\\envs\\humble':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = 'C:\\dev\\p-p_teleop_robotics_unal\\install\\joystick_ros2'

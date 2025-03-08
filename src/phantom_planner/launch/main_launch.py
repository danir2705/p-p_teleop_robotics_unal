# ~/ros2_ws/src/my_python_pkg/launch/launch_node_from_another_pkg.py
import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution


def generate_launch_description():
    joy_node = Node(
        package='phantom_joy',
        executable='talker'
    )

    jacobian_node = Node(
        package='phantom_planner',
        executable='jacobian'
    )

    gui_node = Node(
        package="phantom_planner",
        executable="gui"
    )

    coppelia =   IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('phantom_coppelia'),
                    'launch',
                    'bringup_launch.py'
                ])
            ]))
    

    control =   IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('phantom_control'),
                    'launch',
                    'px100_bringup_launch.py'
                ])
            ]))
    

    return LaunchDescription([
        joy_node,
        jacobian_node, 
        coppelia, 
        control,
        gui_node
    ])

from launch import LaunchDescription
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
import os 

def generate_launch_description():
    
    pkg_dir = get_package_share_directory('phantom_coppelia')
    scene_path = os.path.join(pkg_dir, "scenes", "spheres.ttt")

    qt_plugin_path = os.path.join(os.getenv('PROGRAMFILES'), 'CoppeliaRobotics', 'CoppeliaSimEdu', 'Qt', 'plugins')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_plugin_path



    cmd_str = 'start C:\"Program Files"\CoppeliaRobotics\CoppeliaSimEdu\coppeliaSim.exe'    
    # Make sure each part of the command is passed as a separate list element
    coppelia_node = ExecuteProcess(
        cmd=[[cmd_str, " -f", scene_path, " -s0"]],  # Correct command structure
        shell=True
    )
   
    return LaunchDescription([coppelia_node])
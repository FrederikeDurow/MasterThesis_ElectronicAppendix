# #!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    depthai_pkg_path = os.path.join(get_package_share_directory('depthai_examples'))
    
    # Behavior Tree Node
    behavior_tree = Node(
        package='behavior_tree',
        executable='tree_generator',
        output='screen',
        emulate_tty=True
    )
  

    # Launch them all!
    return LaunchDescription([
        behavior_tree, 
    ])
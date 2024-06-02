# #!/usr/bin/env python3

# ##############################################################################
# # Documentation
# ##############################################################################
# """
# Spot Behavior Tree Launch File
# """
# ##############################################################################
# # Imports
# ##############################################################################
# import launch
# import launch_ros.actions

# ##############################################################################
# # Launch Service
# ##############################################################################


# def generate_launch_description():
#     """
#     Launch description for the tutorial.
#     """
#     #return tg.generate_launch_description()
#     return launch.LaunchDescription(
#         [
#             launch_ros.actions.Node(
#                 package='behavior_tree',
#                 executable="tree_generator",
#                 output='screen',
#                 emulate_tty=True
#             )
#         ]
#     )
#!/usr/bin/env python3

##############################################################################
# Documentation
##############################################################################
"""
Spot Behavior Tree Launch File
"""
##############################################################################
# Imports
##############################################################################

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


##############################################################################
# Launch Service
##############################################################################

def generate_launch_description():

    depthai_pkg_path = os.path.join(get_package_share_directory('depthai_examples'))
    
    # Behavior Tree Node
    behavior_tree = Node(
        package='behavior_tree',
        executable='tree_generator',
        output='screen',
        emulate_tty=True
    )

    # OAK-D Pro Camera and Yolov4
    oak_yolo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(depthai_pkg_path, 'launch', 'yolov4_publisher.launch.py')]), 
        launch_arguments={'spatial_camera': 'true'}.items(),
    )

    # Publishes bounding boxes and labels for detected objects
    label_bb_publisher = Node(
        package='visualization',
        executable='bb_visualization',
        output='screen', 
        name = "label_publisher",
    )

    # Shows OAK Cam view incl. bounding boxes and labels of detected objects
    image_viewer = Node(
        package='rqt_image_view',
        executable='rqt_image_view',
        name='rqt_image_viewer',
        output='screen',
    )

    # Launch them all!
    return LaunchDescription([
        behavior_tree, 
        oak_yolo,
        label_bb_publisher,
        image_viewer
    ])
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node, SetRemap
from launch.actions import IncludeLaunchDescription, GroupAction, DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    config_dir = os.path.join(get_package_share_directory('navigation'),'config')
    param_file = os.path.join(config_dir,'nav2_spot_params[DWB_Planner].yaml') #'nav2_spot_params[DWB_Planner].yaml'
    rviz_config = os.path.join(config_dir,'nav2_spot_4cam.rviz')
    
    #enable_rviz = LaunchConfiguration('rviz')

    return LaunchDescription(
        [
        DeclareLaunchArgument(
            'rviz', default_value='false',
            description='Whenever to launch with rviz or not'),

        GroupAction(
        actions=[

            SetRemap(src='/map',dst='/rtabmap/map'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([get_package_share_directory('nav2_bringup'),'/launch','/navigation_launch.py']),
            launch_arguments={
            'params_file': param_file,
            'autostart':'False',}.items(),
      
    )]),
    # Node(
    #     condition=IfCondition(enable_rviz),
    #     package='rviz2',
    #     executable='rviz2',
    #     name='rviz2_node',
    #     arguments=['-d', rviz_config],
    #     output='screen',
    #     ),
    ])

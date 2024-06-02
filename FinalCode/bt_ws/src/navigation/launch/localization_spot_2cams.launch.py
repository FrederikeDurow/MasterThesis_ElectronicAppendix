

# A maximum of 4 cameras can be synchronized at the same time. If > 1, the rgbd_image topics should contain the camera index starting with 0

import os
import sys
import launch
import launch_ros
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():     

    config_dir = os.path.join(get_package_share_directory('navigation'), 'config')         
    map_dir = os.path.join(get_package_share_directory('navigation'), 'maps')

    rviz_config = os.path.join(config_dir,"localization_spot_2cam.rviz")
    map = os.path.join(map_dir, 'rtabmap_spot_2cam.db') 

    rviz_node = launch_ros.actions.Node(
        package='rviz2', executable='rviz2', output='screen',
        arguments=[["-d"], [rviz_config]]
    )

    # Camera remapping nodes
    spotcam_sync1_node = launch_ros.actions.Node(
        package='rtabmap_sync', executable='rgbd_sync', name='rgbd_sync1', output="screen",
        parameters=[{
            "approx_sync": True,
            "queue_size":100,
            }],
        remappings=[
            ("rgb/image", "/camera/frontleft/image"),
            ("depth/image", "/depth_registered/frontleft/image"),
            ("rgb/camera_info", "/camera/frontleft/camera_info"),
            ("rgbd_image", 'rgbd_image')],
        namespace='spot_camera_frontleft'
    )
    spotcam_sync2_node = launch_ros.actions.Node(
        package='rtabmap_sync', executable='rgbd_sync', name='rgbd_sync2', output="screen",
        parameters=[{
            "approx_sync": True,
            "queue_size":100,
            }],
        remappings=[
            ("rgb/image", "/camera/frontright/image"),
            ("depth/image", "/depth_registered/frontright/image"),
            ("rgb/camera_info", "/camera/frontright/camera_info"),
            ("rgbd_image", 'rgbd_image')],
        namespace='spot_camera_frontright'
    )

    # RGB-D odometry
    rgbd_odometry_node = launch_ros.actions.Node(
        package='rtabmap_odom', executable='rgbd_odometry', output="screen",
        parameters=[{
            "frame_id": 'body', #default base_link try with body
            "odom_frame_id": 'odom', #default odom try with base_link or odometry
            "publish_tf": True, 
            "approx_sync": True,
            "subscribe_rgbd": True,
            "queue_size":100,
            "RGBD/StartAtOrigin": "false",
            "RGBD/MarkerDetection":True,

            "Odom/FilteringStrategy": 2, #"0=No filtering 1=Kalman filtering 2=Particle filtering.
            }],
        remappings=[
            ("rgbd_image", '/spot_camera_frontleft/rgbd_image'),
            ("odom", '/odometry')],
        prefix='',
        namespace='rtabmap'
    )

    # Voxelcloud nodes
    voxelcloud1_node = launch_ros.actions.Node(
        package='rtabmap_util', executable='point_cloud_xyzrgb', name='point_cloud_xyzrgb1', output='screen',
        parameters=[{
            "approx_sync": True,
            "queue_size":100,
            "max_depth":2.0,
            "min_depth":0.1,
            "noise_filter_radius": 0.1,
            "filter_nans":True,
            "voxel_size":0.2,
            "decimation":4,
        }],
        remappings=[
            ("rgb/image", "/camera/frontleft/image"),
            ("depth/image", "/depth_registered/frontleft/image"),
            ("rgb/camera_info", "/camera/frontleft/camera_info"),
            ('rgbd_image', 'rgbd_image'),
            ('cloud', 'voxel_cloud1')]
    )
    voxelcloud2_node = launch_ros.actions.Node(
        package='rtabmap_util', executable='point_cloud_xyzrgb', name='point_cloud_xyzrgb2', output='screen',
        parameters=[{
            "approx_sync": True,
            "queue_size":100,
            "max_depth":2.0,
            "min_depth":0.1,
            "noise_filter_radius": 0.1,
            "filter_nans":True,
            "voxel_size":0.2,
            "decimation":4,
        }],
        remappings=[
            ("rgb/image", "/camera/frontright/image"),
            ("depth/image", "/depth_registered/frontright/image"),
            ("rgb/camera_info", "/camera/frontright/camera_info"),
            ('rgbd_image', 'rgbd_image'),
            ('cloud', 'voxel_cloud2')]
    )
    # SLAM 
    slam_node = launch_ros.actions.Node(
        package='rtabmap_slam', executable='rtabmap', output="screen",
        parameters=[{
            "rgbd_cameras":2,
            "subscribe_depth": True,
            "subscribe_rgbd": True,
            "subscribe_rgb": True,
            "subscribe_odom_info": True,
            "approx_sync_max_interval":0.5,
            "queue_size":100,
            "odom_sensor_sync": True, #added by me
            "frame_id": 'body',
            "map_frame_id": 'map',
            "publish_tf": True,
            'Reg/Force3DoF':'true',
            "database_path": map,
            "approx_sync": True,
            "Mem/IncrementalMemory": "False",
            "Mem/InitWMWithAllNodes": "True",
            "use_action_for_goal": True,
             #added by me (MONDAY EVENING )
            'Reg/Force3DoF':'true',
            'RGBD/NeighborLinkRefining':'True',
            #"icp_odometry": True,
            "Reg/Strategy": '2', #0=TORO, 1=g2o and 2=GTSAM
            'Optimizer/GravitySigma':'0.3', # Disable imu constraints (we are already in 2D)
            'proj_max_ground_height':'0.1', #ncreasing the proj_max_ground_height will make the algorithm ignore points that are under this threshold while projection. All points below this threshold will be ignored:
            "proj_max_height":"2.0", #proj_max_height means mapping maxim
            "RGBD/StartAtOrigin": "false", 
            "RGBD/MarkerDetection":True,

            "Odom/FilteringStrategy": 2, #"0=No filtering 1=Kalman filtering 2=Particle filtering.
        }],
        remappings=[
            # Has to start from 0 and go up
            ("rgbd_image0", '/spot_camera_frontleft/rgbd_image'),
            ("rgbd_image1", '/spot_camera_frontright/rgbd_image'),
            ("odom", '/odometry')],
        prefix='',
        namespace='rtabmap'
    )
    return launch.LaunchDescription(
        [
        spotcam_sync1_node,
        spotcam_sync2_node,
        rgbd_odometry_node,
        slam_node,
        voxelcloud1_node,
        voxelcloud2_node,
        rviz_node,
        #rtabmap_rviz_node,
        ]
    )



    #rtabmap_rviz_node = launch_ros.actions.Node(
    #        package='rtabmap_viz', executable='rtabmap_viz', output='screen',
    #        remappings=[
    #        # Has to start from 0 and go up
    #        ("rgbd_image0", '/spot_camera_frontleft/rgbd_image'),
    #        ("rgbd_image1", '/spot_camera_frontright/rgbd_image'),
    #        ("odom", '/odometry')],
    #)


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

    rviz_config = os.path.join(config_dir,"localization_spot_4cam.rviz")
    map = os.path.join(map_dir, 'rtabmap_spot_4cam.db') 

    enable_rviz = LaunchConfiguration('rviz')

    rviz_node = launch_ros.actions.Node(
        condition=IfCondition(enable_rviz),
        package='rviz2', executable='rviz2', output='screen',
        arguments=[["-d"], [rviz_config]]
    )

    # Camera remapping nodes
    spotcam_sync1_node = launch_ros.actions.Node(
        package='rtabmap_sync', executable='rgbd_sync', name='rgbd_sync1', output="screen",
        parameters=[{
            "approx_sync": True,
            "queue_size":100,
            #"decimation":2,
            }],
        remappings=[
            ("rgb/image", "/camera/frontleft/image"),
            ("depth/image", "/depth_registered/frontleft/image"),
            ("rgb/camera_info", "/camera/frontleft/camera_info"),
            ("rgbd_image", 'rgbd_image')], #Not sure what is meant here
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
            ("rgbd_image", 'rgbd_image')], #Not sure what is meant here
        namespace='spot_camera_frontright'
    )
    spotcam_sync3_node = launch_ros.actions.Node(
        package='rtabmap_sync', executable='rgbd_sync', name='rgbd_sync3', output="screen",
        parameters=[{
            "approx_sync": True,
            "queue_size":100,
            }],
        remappings=[
            ("rgb/image", "/camera/left/image"),
            ("depth/image", "/depth_registered/left/image"),
            ("rgb/camera_info", "/camera/left/camera_info"),
            ("rgbd_image", 'rgbd_image')], #Not sure what is meant here
        namespace='spot_camera_left'
    )
    spotcam_sync4_node = launch_ros.actions.Node(
        package='rtabmap_sync', executable='rgbd_sync', name='rgbd_sync4', output="screen",
        parameters=[{
            "approx_sync": True,
            "queue_size":100,
            }],
        remappings=[
            ("rgb/image", "/camera/right/image"),
            ("depth/image", "/depth_registered/right/image"),
            ("rgb/camera_info", "/camera/right/camera_info"),
            ("rgbd_image", 'rgbd_image')], #Not sure what is meant here
        namespace='spot_camera_right'
    )

    # RGB-D odometry
    rgbd_odometry_node = launch_ros.actions.Node(
        package='rtabmap_odom', executable='rgbd_odometry', output="screen",
        parameters=[{
            "frame_id": 'body',
            "odom_frame_id": 'odom',
            "publish_tf": True, 
            "approx_sync": True,
            "subscribe_rgbd": True,
            "queue_size":100,
            "RGBD/StartAtOrigin": "false",
            #"RGBD/MarkerDetection":"True",
            "Odom/AlignWithGround": "True",
            #"Odom/ImageDecimation": "2",
            "Vis/EstimationType": "0",
            "Vis/MinDepth": "0.1",
            "Vis/MinInliers": "15",
            ####"RGBD/MaxOdomCacheSize": "20"  
            "Reg/Strategy": "0" #0=vis, 1=icp, 2=VisIcp
            #"Odom/FilteringStrategy": 1, #"0=No filtering 1=Kalman filtering 2=Particle filtering.

            }],
        remappings=[
            # Has to start from 0 and go up
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
            "noise_filter_min_neighbors":5,
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
            "noise_filter_min_neighbors":5,
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

    voxelcloud3_node = launch_ros.actions.Node(
        package='rtabmap_util', executable='point_cloud_xyzrgb', name='point_cloud_xyzrgb3', output='screen',
        parameters=[{
            "approx_sync": True,
            "queue_size":100,
            "max_depth":2.0,
            "min_depth":0.1,
            "noise_filter_radius": 0.1,
            "noise_filter_min_neighbors":5,
            "filter_nans":True,
            "voxel_size":0.2,
            "decimation":4,
        }],
        remappings=[
            ("rgb/image", "/camera/left/image"),
            ("depth/image", "/depth_registered/left/image"),
            ("rgb/camera_info", "/camera/left/camera_info"),
            ('rgbd_image', 'rgbd_image'),
            ('cloud', 'voxel_cloud3')]
    )   
    voxelcloud4_node = launch_ros.actions.Node(
        package='rtabmap_util', executable='point_cloud_xyzrgb', name='point_cloud_xyzrgb4', output='screen',
        parameters=[{
            "approx_sync": True,
            "queue_size":100,
            "max_depth":2.0,
            "min_depth":0.1,
            "noise_filter_radius": 0.1,
            "noise_filter_min_neighbors":5,
            "filter_nans":True,
            "voxel_size":0.2,
            "decimation":2,
        }],
        remappings=[
            ("rgb/image", "/camera/right/image"),
            ("depth/image", "/depth_registered/right/image"),
            ("rgb/camera_info", "/camera/right/camera_info"),
            ('rgbd_image', 'rgbd_image'),
            ('cloud', 'voxel_cloud4')]
    )  

    # SLAM 
    slam_node = launch_ros.actions.Node(
        package='rtabmap_slam', executable='rtabmap', output="screen",
        parameters=[{
            "rgbd_cameras":4,
            #"subscribe_depth": True,
            "subscribe_rgbd": True,
            "subscribe_rgb": True,
            "subscribe_odom_info": True,
            "approx_sync_max_interval":0.7, 
            "queue_size":100,
            "odom_sensor_sync": True, #added by me
            "frame_id": 'body',
            "map_frame_id": 'map',
            "publish_tf": True,
            "database_path": map,
            "approx_sync": True,
            "Mem/IncrementalMemory": "False",
            "Mem/InitWMWithAllNodes": "True",
            "use_action_for_goal": True,
             #added by me (MONDAY EVENING )
            'Reg/Force3DoF':'true', # Maybe try 6dof (have to be in the mapping aswell)
            'RGBD/NeighborLinkRefining':'True',
            "Reg/Strategy": '0', #0=TORO, 1=g2o and 2=GTSAM should be 0 maybe
            'Optimizer/GravitySigma':'0.3', # Disable imu constraints (we are already in 2D)
            'proj_max_ground_height':'0.1', #ncreasing the proj_max_ground_height will make the algorithm ignore points that are under this threshold while projection. All points below this threshold will be ignored:
            "proj_max_height":"2.0",
            "RGBD/StartAtOrigin": "False",
            #"RGBD/MarkerDetection":"True",
            #"Marker/Dictionary":"20",
            #"Marker/Length":"0.146",
            #"RGBD/CreateOccupancyGrid": "False",

            "Mem/BinDataKept": "False",   # NEW
            "Rtabmap/DetectionRate": "5", # NEW previously set to 1
            "Vis/EstimationType": "0",
            #'Grid/3D':'False',
            #'Grid/RayTracing':'True',
            "Vis/MinInliers": "15", 
            #'Grid/NormalsSegmentation':'True',
            #'Grid/MaxGroundHeight':"0.2",
            "Vis/MinDepth": "0.1"
            ####"RGBD/MaxOdomCacheSize": "20"  
            #"Odom/FilteringStrategy": 1, #"0=No filtering 1=Kalman filtering 2=Particle filtering.
        }],
        remappings=[
            # Has to start from 0 and go up
            ("rgbd_image0", '/spot_camera_frontleft/rgbd_image'),
            ("rgbd_image1", '/spot_camera_frontright/rgbd_image'),
            ("rgbd_image2", '/spot_camera_left/rgbd_image'),
            ("rgbd_image3", '/spot_camera_right/rgbd_image'),
            ("odom", '/odometry')],
        prefix='',
        namespace='rtabmap'
    )

    return launch.LaunchDescription(
        [
        DeclareLaunchArgument(
          'rviz', default_value='true',
          description='Whenever to launch with rviz or not'),

        spotcam_sync1_node,
        spotcam_sync2_node,
        spotcam_sync3_node,
        spotcam_sync4_node,
        rgbd_odometry_node,
        slam_node,
        voxelcloud1_node,
        voxelcloud2_node,
        voxelcloud3_node,
        voxelcloud4_node,
        rviz_node,
        ]
    )
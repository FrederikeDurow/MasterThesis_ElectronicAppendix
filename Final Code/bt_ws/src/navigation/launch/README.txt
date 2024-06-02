########## FILES ##########

(OPTIMIZING SEE NOTE): rtabmap_spot_1cam.launch.py (Uses OAK-D pro)
(UNDER DEVELOPMENT): rtabmap_spot_2cams.launch.py (Uses Spot's 2 front cameras)
(UNDER DEVELOPMENT): rtabmap_spot_4cams.launch.py (Uses Spot's 2 front cameras and the LEFT and RIGHT)

########## OPTIMIZING NOTES ##########

- Get the IMU to work for better mapping in the rtabmap_spot_1cam
    a. IMU added and it is running, though i get: 
        [imu_filter_madgwick_node-2] 2024-01-19 21:27:57.130 [RTPS_TRANSPORT_SHM Error] Failed init_port fastrtps_port7421: open_and_lock_file failed -> Function open_port_internal
        [imu_filter_madgwick_node-2] 2024-01-19 21:27:57.130 [RTPS_TRANSPORT_SHM Error] Failed init_port fastrtps_port7423: open_and_lock_file failed -> Function open_port_internal


- Set up a "map" and "config" folder with all the standard parameters in


########## GENERAL NOTES ##########

After mapping call: "rtabmap-databaseViewer ~/.ros/rtabmap.db" to see map

Spots mapping is way better with ethernet connects.
Check the tf for Spot, the missing key.


NOTE: they all create their map in ~/.ros/rtabmap.db (something like this)


#####################################
These was under the rtabmap_slam parameters, maybe they could fix Spot?

~wait_for_transform (bool, default: "true")
Wait (maximum wait_for_transform_duration sec) for transform when a tf transform is not still available.

~wait_for_transform_duration (double, default: 0.1)
Wait duration for wait_for_transform.

#####################################
For navigation: 
- in the rtabmap_ros there is an example of using turtlebot3
	demos/launch/turtlebot3_rgbd.launch.py
	
then to navigate one has to call: 
	#   Navigation (install nav2_bringup package):
#     $ ros2 launch nav2_bringup navigation_launch.py use_sim_time:=True
#     $ ros2 launch nav2_bringup rviz_launch.py

so might be able to "reverse-engineer" this


https://github.com/introlab/rtabmap_ros/issues/775

#####################################
[ERROR] (2024-01-30 11:31:38.030) RegistrationVis.cpp:1575::computeTransformationImpl() Multi-camera 2D-3D PnP registration is only available if rtabmap is built with OpenGV dependency. Use 3D-3D registration approach instead for multi-camera.
#######################################
Date Feb 18

Maybe turn of the 3D map in localization mode: 

#ifdef RTABMAP_OCTOMAP
    RTABMAP_PARAM(Grid, 3D,                      bool,   true,    uFormat("A 3D occupancy grid is required if you want an OctoMap (3D ray tracing). Set to false if you want only a 2D map, the cloud will be projected on xy plane. A 2D map can be still generated if checked, but it requires more memory and time to generate it. Ignored if laser scan is 2D and \"%s\" is 0.", kGridSensor().c_str()));
#else
    RTABMAP_PARAM(Grid, 3D,                      bool,   false,   uFormat("A 3D occupancy grid is required if you want an OctoMap (3D ray tracing). Set to false if you want only a 2D map, the cloud will be projected on xy plane. A 2D map can be still generated if checked, but it requires more memory and time to generate it. Ignored if laser scan is 2D and \"%s\" is 0.", kGridSensor().c_str()));
#endif


    RTABMAP_PARAM(Mem, SaveDepth16Format,           bool, false,    "Save depth image into 16 bits format to reduce memory used. Warning: values over ~65 meters are ignored (maximum 65535 millimeters).");


    RTABMAP_PARAM(Mem, InitWMWithAllNodes,          bool, false,    "Initialize the Working Memory with all nodes in Long-Term Memory. When false, it is initialized with nodes of the previous session.");

    RTABMAP_PARAM(Kp, ByteToFloat,              bool, false,  uFormat("For %s=1, binary descriptors are converted to float by converting each byte to float instead of converting each bit to float. When converting bytes instead of bits, less memory is used and search is faster at the cost of slightly less accurate matching.", kKpNNStrategy().c_str()));


Maybe fixes the flying bug?:
    RTABMAP_PARAM(Odom, AlignWithGround,        bool, false,  "Align odometry with the ground on initialization.");

Increase speed:
    RTABMAP_PARAM(FAST, Gpu,                bool, false,  "GPU-FAST: Use GPU version of FAST. This option is enabled only if OpenCV is built with CUDA and GPUs are detected.");


############# NETWORK ADDITION
https://dev.bostondynamics.com/docs/concepts/networking
"Applications can be deployed on computers that physically connect to Spot via the rear RJ-45 port, the DB-25 payload port, 
or the RJ-45 port on a Spot GXP payload. This provides a reliable, high-rate communications link without infrastructure requirements, 
but limits where the application can be run."

I cannot find any direct conclusion that the Spot GXP payload is indeed faster than the rear-ethernet-port. However, as seen in above "without infrastructure requirements" could potentially mean no overhead? But again i cannot confirm it.



The below show how to setup the GXP 
https://support.bostondynamics.com/s/article/Spot-General-Expansion-Payload-GXP


Det ligner de har opdateret ros2 wrapperen fra 3.20 til 3.3.2






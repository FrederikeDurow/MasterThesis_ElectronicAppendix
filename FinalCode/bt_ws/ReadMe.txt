To use this code, a number of other packages need to be installed. 
The most important one is the Spot_ros2 wrapper. 
It can be cloned from https://github.com/bdaiinstitute/spot_ros2 into bt_ws/src/spot/


*********** Run Spot Driver, localization and navigation ***********
ros2 launch spot_driver spot_driver.launch.py
ros2 launch navigation localization_spot_4cams.launch.py
ros2 launch navigation navigation.launch.py

*********** Run Behavior Tree ***********
ros2 launch behavior_tree behavior_tree_launch.py


*********** Mapping ***********
ros2 launch command_center rtabmap_spot_4cams.launch.py 


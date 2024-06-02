import subprocess
import os
import time

def launch_in_terminal(package, launch_file, args):
    cmd = f"ros2 launch {package} {launch_file} {' '.join(args)}"
    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', cmd])

if __name__ == '__main__':
    # Replace 'your_package_name' with the actual name of your ROS 2 package

    # Define arguments for each launch file
    args_launch_foxglove= []
    args_launch_spot_driver = []
    args_launch_localization = ["rviz:=false"]
    args_launch_navigation = ["rviz:=false"]
    args_launch_behavior_tree = []

    # Starts the Foxglove
    launch_in_terminal('behavior_tree', 'foxglove_launch.xml', args_launch_foxglove)

    # Starts the spot driver
    launch_in_terminal('spot_driver', 'spot_driver.launch.py', args_launch_localization)

    # Wait for a short time 
    time.sleep(2)

    # Starts the localization (RTABMAP)
    launch_in_terminal('navigation', 'localization_spot_4cams.launch.py', args_launch_localization)

    # Wait for a short time 
    time.sleep(2)

    # Starts the navigation (Nav2)
    launch_in_terminal('navigation', 'navigation.launch.py', args_launch_navigation)

    # Wait for a short time
    time.sleep(6)

    launch_in_terminal('behavior_tree', 'behavior_tree_launch.py', args_launch_behavior_tree)

    # Keep the script running
    input("Press Enter to exit...")
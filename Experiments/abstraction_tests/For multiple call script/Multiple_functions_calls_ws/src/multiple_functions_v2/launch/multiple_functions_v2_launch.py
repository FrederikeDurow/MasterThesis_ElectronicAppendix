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
import launch
import launch_ros.actions

##############################################################################
# Launch Service
##############################################################################


def generate_launch_description():
    """
    Launch description for the tutorial.
    """
    #return tg.generate_launch_description()
    return launch.LaunchDescription(
        [
            launch_ros.actions.Node(
                package='multiple_functions_v2',
                executable="tree_generator",
                output='screen',
                emulate_tty=True
            )
        ]
    )

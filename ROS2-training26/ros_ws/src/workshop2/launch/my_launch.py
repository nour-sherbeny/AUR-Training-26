import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    package_path = get_package_share_directory('workshop2')

    parameter_file = os.path.join(
        package_path,
        'config',
        'task1Param.yaml'
    )

    return LaunchDescription([

        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim'
        ),

        Node(
            package='workshop2',
            executable='task1',
            name='service_client'
        ),

        Node(
            package='workshop2',
            executable='task2',
            name='go_to_goal',
            parameters=[parameter_file]
        ),

    ])
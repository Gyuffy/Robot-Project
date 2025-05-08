from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription(
        [
            Node(
                package="rs_camera",
                executable="image_publisher",
                output="screen",
            )
        ]
    )

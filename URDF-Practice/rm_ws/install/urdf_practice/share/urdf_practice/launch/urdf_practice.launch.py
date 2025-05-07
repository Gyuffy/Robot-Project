from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    rviz_config_file = '/home/ssafy/rm_ws/src/urdf_practice/rviz/urdf_practice.rviz'

    urdf_file = '/home/ssafy/rm_ws/src/urdf_practice/urdf/simple_robot.urdf'

    with open(urdf_file, 'r') as infp:
        robot_description = infp.read()

    return LaunchDescription([
        Node(
            package = 'robot_state_publisher',
            executable = 'robot_state_publisher',
            output = 'screen',
            parameters = [{'robot_description': robot_description}]
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rvize2',
            output = 'screen',
            arguments=['-d', rviz_config_file]
        )
    ])
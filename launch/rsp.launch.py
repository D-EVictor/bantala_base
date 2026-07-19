import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch_ros.actions import Node

import xacro


def launch_setup(context, *args, **kwargs):

    use_sim_time = LaunchConfiguration('use_sim_time')
    use_ros2_control = LaunchConfiguration('use_ros2_control').perform(context)
    sim_mode = LaunchConfiguration('sim_mode').perform(context)

    pkg_path = os.path.join(get_package_share_directory('bantala_base'))
    xacro_file = os.path.join(pkg_path, 'description', 'robot.urdf.xacro')
    robot_description_config = xacro.process_file(
        xacro_file,
        mappings={
            'use_ros2_control': use_ros2_control,
            'sim_mode': sim_mode
        }
    ).toxml()

    params = {'robot_description': robot_description_config, 'use_sim_time': use_sim_time}
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    return [node_robot_state_publisher]


def generate_launch_description():

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false', description='Use sim time if true'),
        DeclareLaunchArgument('use_ros2_control', default_value='true', description='Use ros2_control if true'),
        DeclareLaunchArgument('sim_mode', default_value='false', description='Run in simulation mode if true'),

        OpaqueFunction(function=launch_setup)
    ])